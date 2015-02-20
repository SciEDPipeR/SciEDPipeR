
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import bz2
import gzip
import logging
import os
import Pipeline
import shutil
import tarfile
import zipfile

# Types of compression supported
STR_COMPRESSION_BZ2 = "bz2"
STR_COMPRESSION_GZ = "gz"
STR_COMPRESSION_ZIP = "zip"
LSTR_COMPRESSION_CHOICES = [ STR_COMPRESSION_BZ2, STR_COMPRESSION_GZ, STR_COMPRESSION_ZIP ]

# Types of compression recognized but not supported
STR_COMPRESSION_TAR_Z = "tarz"
STR_COMPRESSION_LZH_ZIP = "LZHZIP"

STR_COMPRESSION_ARCHIVE = "archive"
STR_COMPRESSION_FIRST_LEVEL_ONLY = "level1"
LSTR_COMPRESSION_MODE_CHOICES = [ STR_COMPRESSION_ARCHIVE, STR_COMPRESSION_FIRST_LEVEL_ONLY ]

class Compression:
    """
    Collects functions associated with compression.
    """
    
    def __init__( self, logr_cur = None ):
        """
        Initializer
        """
        
        self.logr_logger = logging.getLogger() if not logr_cur else logr_cur
        """ Logger, uses the default logger. """
        
        self.dict_magic_number = { "\x1f\x8b\x08": STR_COMPRESSION_GZ,
                                   "\x42\x5a\x68": STR_COMPRESSION_BZ2,
                                   "\x50\x4b\x03\x04": STR_COMPRESSION_ZIP,
                                   "\x50\x4b\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00": STR_COMPRESSION_ZIP,
                                   "\x50\x4b\x07\x08": STR_COMPRESSION_ZIP,
                                   "\x1f\x9d:": STR_COMPRESSION_TAR_Z,
                                   "\x1f\xa0:": STR_COMPRESSION_LZH_ZIP }
        """ Holds the magic numbers to compression schemes to detect them """

        self.i_max_length = max( len( str_key ) for str_key in self.dict_magic_number )
        """ Max length of the magic numbers """
    
    # Tested 5 tests 2-12-2015
    def func_compress( self, str_file_path, str_output_directory, str_compression_type = STR_COMPRESSION_GZ, 
                       str_compression_mode = STR_COMPRESSION_ARCHIVE, f_test = False ):
        """
        Convenience function which compresses a file path 
        (file or directory; gz and bz2 directory are first tarred).
    
        * str_file_path : Path of file or folder to compress.
                        : String
        * str_output_directory : Path of the projct's output directory. Files must be in the output directory
                                 in order to be compressed.
                               : String Absolute Path
        * str_compression_type : String indicator of the compression to use.
                               : A value from Compression.COMPRESION_CHOICES
        * str_compression_mode : String indicator on how compression should occur.
                                 Compression.STR_COMPRESSION_ARCHIVE archives a directory as one compressed unit.
                                 Compression.STR_COMPRESSION_FIRST_LEVEL_ONLY archives each item in the directory's root level.
                                 File are not affected by str_compression_mode and are simply compressed.
                               : Compression.STR_COMPRESSION_ARCHIVE and Compression.STR_COMPRESSION_FIRST_LEVEL_ONLY
        * f_test : Indicates to run in test mode (True) or not
                 : Boolean
        * return : Returns a None on failure or the path of the compressed file or directory
                 : Boolean or String
        """
        
        # Pipeline function used to check if a file is valid to be removed (after compression)
        cur_pipeline = Pipeline.Pipeline()
        
        # Make sure the choice was a compression that is handled
        if not str_compression_type in LSTR_COMPRESSION_CHOICES:
            self.logr_logger.error( "func_compress: Please indicate a compression type from the following choices: " + 
                                    ",".join( LSTR_COMPRESSION_CHOICES ) + "." )
            return None
        
        # make sure the mode choices are valid
        if not str_compression_mode in LSTR_COMPRESSION_MODE_CHOICES:
            self.logr_logger.error( "func_compress: Please indicate a compression type from the following choices: " + 
                                    ",".join( LSTR_COMPRESSION_MODE_CHOICES ) + "." )
            return None
        
        # Check if it exists
        if not str_file_path or not os.path.exists( str_file_path ):
            self.logr_logger.error( "func_compress: The following path to compress does not exist: " + 
                                    "None" if str_file_path is None else str_file_path )
            return None
        
        # Check if it is already compressed
        if self.func_is_compressed( str_file_path ):
            self.logr_logger.info( "func_compress: The following path was already compressed: " + str_file_path )
            return str_file_path
        
        # Zip archiving is a different pattern so handled separately
        if str_compression_type == STR_COMPRESSION_ZIP:
            i_zip_mode = None
            try:
                import zlib
                i_zip_mode = zipfile.ZIP_DEFLATED
            except:
                i_zip_mode = zipfile.ZIP_STORED
                self.logr_logger.error( "func_compress: Zlib python library is needed to make ZIp archives, " + 
                                          "please make sure it is installed or select another compression type." )
                return None
            
            str_compressed_archive = str_file_path
            if str_compression_mode == STR_COMPRESSION_ARCHIVE:
                str_compressed_archive = str_compressed_archive + "." + STR_COMPRESSION_ZIP

            self.logr_logger.info( "func_compress: Will attempt to compress the following path with ZIP compression:" + 
                                       str_compressed_archive )
            if not f_test:
                # Make the list of folders and files to compress
                # Archive mode
                lstr_paths = [ str_file_path ]
                if os.path.isdir( str_file_path ) and ( str_compression_mode == STR_COMPRESSION_FIRST_LEVEL_ONLY ):
                    lstr_paths = [ os.path.join( str_file_path, str_path ) for str_path in os.listdir( str_file_path ) ]
                
                for str_path_to_compress in lstr_paths:
                    # The name of the new compressed zip archive
                    str_compressed_dir_name = str_path_to_compress + "." + STR_COMPRESSION_ZIP
                    hndl_compressed_dir = zipfile.ZipFile( str_compressed_dir_name, 
                                                           mode = "w", 
                                                           allowZip64 = True,
                                                           compression = i_zip_mode )
                    
                    if os.path.isdir( str_path_to_compress ):
                        for str_root, lstr_dirs, lstr_files in os.walk( str_path_to_compress ):
                            for str_file in lstr_files:
                                hndl_compressed_dir.write( filename = os.path.join( str_root, str_file ),
                                                           arcname = os.path.basename( str_file ) )
                    else:
                        hndl_compressed_dir.write( filename = str_path_to_compress,
                                                   arcname = os.path.basename( str_path_to_compress ) )
                    hndl_compressed_dir.close()

                # At successful archive creation
                # Check that the files are valid before trying to delete them
                f_remove_files = True
                for str_path_to_compress in lstr_paths:
                    if not cur_pipeline.func_is_valid_path_for_removal( str_path = str_path_to_compress,
                                                                 str_output_directory = str_output_directory ):
                        self.logr_logger.info( "func_compress: Could not remove originals after compression. Problematic path = " + str_path_to_compress )
                        f_remove_files = False
                # Now remove originals
                if f_remove_files:
                    for str_path_to_compress in lstr_paths:
                        if os.path.isfile( str_path_to_compress ):
                            os.remove( str_path_to_compress )
                        else:
                            shutil.rmtree( str_path_to_compress )
                else:
                    return None

            return str_compressed_archive

        # Handle gz and bz2
        # Check if it is a file or folder
        if os.path.isdir( str_file_path ):
            # tar.gz and tar.bz2
            str_compressed_dir_name = str_file_path + ".tar."+ str_compression_type
            str_compression_open_mode = "w:bz2" if str_compression_type == STR_COMPRESSION_BZ2 else "w:gz"
            
            if str_compression_mode == STR_COMPRESSION_FIRST_LEVEL_ONLY:
                self.logr_logger.info( "func_compress: Will attempt to compress the contents of the following directory with " + 
                                       str_compression_type + " compression: " + str_file_path )
                if f_test: 
                    return str_file_path
            elif str_compression_mode == STR_COMPRESSION_ARCHIVE:
                self.logr_logger.info( "func_compress: Will attempt to compress the following directory with " + 
                                       str_compression_type + " compression: " + str_compressed_dir_name )
                if f_test:
                    return str_compressed_dir_name
            else:
                self.logr_logger.info( "func_compress: Unknown compression mode: " + str_compression_mode )
                if f_test:
                    return None

            hndl_compressed_dir = None
            # Files to compress
            lstr_compress_files = [ str_file_path ]
            if str_compression_mode == STR_COMPRESSION_FIRST_LEVEL_ONLY:
                lstr_compress_files = [ os.path.join( str_file_path, str_file_to_compress ) 
                                       for str_file_to_compress in os.listdir( str_file_path ) ]
                str_compressed_dir_name = str_file_path
            for str_cur_compress_file in lstr_compress_files:
                hndl_compressed_dir = tarfile.open( str_cur_compress_file + ".tar." + str_compression_type, str_compression_open_mode )
                hndl_compressed_dir.add( str_cur_compress_file, arcname = os.path.basename( str_cur_compress_file ) )
                hndl_compressed_dir.close()
                
            # At successful archive creation
            # Check that the files are valid before trying to delete them
            f_remove_files = True
            for str_cur_compress_file in lstr_compress_files:
                if not cur_pipeline.func_is_valid_path_for_removal( str_path = str_cur_compress_file,
                                                                 str_output_directory = str_output_directory ):
                    self.logr_logger.info( "func_compress: Could not remove originals after compression. Problematic path = " + str_path_to_compress )
                    f_remove_files = False
            if f_remove_files:
                for str_cur_compress_file in lstr_compress_files:
                    if os.path.isfile( str_cur_compress_file ):
                        if not f_test:
                            os.remove( str_cur_compress_file )
                    else:
                        if not f_test:
                            shutil.rmtree( str_cur_compress_file )
            else:
                return None          
            return str_compressed_dir_name
        else:
            # Compress files not directories
            # Gz file
            str_compressed_file_name = str_file_path + "." + str_compression_type
            self.logr_logger.info( "func_compress: Will attempt to compress the following file with " + 
                                       str_compression_type + " compression." )
            if f_test:
                return str_compressed_file_name
            with open( str_file_path, "rb" ) as hndl_file_in:
                if str_compression_type == STR_COMPRESSION_GZ:
                    with gzip.open( str_compressed_file_name, "wb" ) as hndl_gz:
                        hndl_gz.writelines( hndl_file_in )
                elif str_compression_type == STR_COMPRESSION_BZ2:
                    with bz2.BZ2File( str_compressed_file_name, mode = "w" ) as hndl_bz:
                        hndl_bz.writelines( hndl_file_in )
            if not cur_pipeline.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                str_output_directory = str_output_directory ):
                self.logr_logger.info( "func_compress: Could not remove originals after compression (bz2/gz). Problematic path = " + str_file_path )
                return None
            else:
                if not f_test:
                    os.remove( str_file_path )
            return str_compressed_file_name
        return None                

    # Tested 13 tests 2-16-2015
    def func_is_compressed( self, str_file_path ):
        """
        Checks if a path to a file or directory is compressed.
        This supports gz, bz2, and zip
        
        Thanks to Lauritz V. Thaulow on stack over flow for their excellent answer
        http://stackoverflow.com/questions/13044562/python-mechanism-to-identify-compressed-file-type-and-uncompress
        
        * str_file_path : Path to file or directory that is potentially compressed
                        : String
        * return : Returns True on compressed and False on not detected as compressed. None is returned if the path is bad.
                 : boolean or None
        """
        
        # Make sure the path is valid
        if not str_file_path or not os.path.exists( str_file_path ):
            self.logr_logger.error( "func_is_compressed: The following path to check compression does not exist: " + 
                                    "None" if str_file_path is None else str_file_path )
            return None
        
        # Handle the case of the uncompressed directory
        if os.path.isdir( str_file_path ):
            self.logr_logger.info( "func_is_compressed: The following path is an uncompressed directory: " + str_file_path )
            return False
        
        # Check for compression
        with open( str_file_path ) as hndl_unknown:
            str_file_start = hndl_unknown.read( self.i_max_length )
            for str_magic_number in self.dict_magic_number:
                if str_file_start.startswith( str_magic_number ):
                    self.logr_logger.info( "func_is_compressed: Compressed" )
                    return True
        self.logr_logger.info( "func_is_compressed: NOT Compressed" )
        return False