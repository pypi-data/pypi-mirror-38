/*
 * Name hash functions
 *
 * Copyright (C) 2018, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <memory.h>
#include <types.h>

#if defined( HAVE_WCTYPE_H )
#include <wctype.h>
#endif

#include "libfsapfs_checksum.h"
#include "libfsapfs_libcerror.h"
#include "libfsapfs_libcnotify.h"
#include "libfsapfs_libuna.h"

/* Calculates the name hash of an UTF-8 formatted string
 * Returns 1 if successful or -1 on error
 */
int libfsapfs_name_hash_calculate_from_utf8_string(
     uint32_t *name_hash,
     const uint8_t *utf8_string,
     size_t utf8_string_length,
     uint8_t use_case_folding,
     libcerror_error_t **error )
{
	uint8_t *utf32_stream                        = NULL;
	static char *function                        = "libfsapfs_name_hash_calculate_from_utf8_string";
	size_t utf32_stream_index                    = 0;
	size_t utf32_stream_size                     = 0;
	size_t utf8_string_index                     = 0;
	libuna_unicode_character_t unicode_character = 0;
	uint32_t calculated_checksum                 = 0;

	if( name_hash == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid name hash.",
		 function );

		return( -1 );
	}
	if( libuna_utf32_stream_size_from_utf8(
	     utf8_string,
	     utf8_string_length,
	     &utf32_stream_size,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve UTF-32 stream size.",
		 function );

		goto on_error;
	}
	utf32_stream_size -= 4;

	utf32_stream = (uint8_t *) memory_allocate(
	                            sizeof( uint8_t ) * utf32_stream_size );

	if( utf32_stream == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_MEMORY,
		 LIBCERROR_MEMORY_ERROR_INSUFFICIENT,
		 "%s: unable to create UTF-32 stream.",
		 function );

		goto on_error;
	}
	while( utf8_string_index < utf8_string_length )
	{
		if( libuna_unicode_character_copy_from_utf8(
		     &unicode_character,
		     utf8_string,
		     utf8_string_length,
		     &utf8_string_index,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_CONVERSION,
			 LIBCERROR_CONVERSION_ERROR_INPUT_FAILED,
			 "%s: unable to copy Unicode character from UTF-8 string.",
			 function );

			goto on_error;
		}
/* TODO add NFD support */
		if( use_case_folding != 0 )
		{
/* TODO add case folding */
			unicode_character  = towlower( unicode_character );
		}
		if( libuna_unicode_character_copy_to_utf32_stream(
		     unicode_character,
		     utf32_stream,
		     utf32_stream_size,
		     &utf32_stream_index,
		     LIBUNA_ENDIAN_LITTLE,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_CONVERSION,
			 LIBCERROR_CONVERSION_ERROR_OUTPUT_FAILED,
			 "%s: unable to copy Unicode character to UTF-32 stream.",
			 function );

			goto on_error;
		}
		if( unicode_character == 0 )
		{
			break;
		}
	}
#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: UTF-32 stream data:\n",
		 function );
		libcnotify_print_data(
		 utf32_stream,
		 utf32_stream_size,
		 LIBCNOTIFY_PRINT_DATA_FLAG_GROUP_DATA );
	}
#endif
	if( libfsapfs_checksum_calculate_weak_crc32(
	     &calculated_checksum,
	     utf32_stream,
	     utf32_stream_size,
	     0xffffffffUL,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_SET_FAILED,
		 "%s: unable to calculate CRC-32.",
		 function );

		goto on_error;
	}
	memory_free(
	 utf32_stream );

	*name_hash = calculated_checksum & 0x003fffffUL;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: CRC-32 checkum\t\t: 0x%08" PRIx32 "\n",
		 function,
		 calculated_checksum );

		libcnotify_printf(
		 "%s: name hash\t\t: 0x%06" PRIx32 "\n",
		 function,
		 *name_hash );

		libcnotify_printf(
		 "\n" );
	}
#endif /* defined( HAVE_DEBUG_OUTPUT ) */

	return( 1 );

on_error:
	if( utf32_stream != NULL )
	{
		memory_free(
		 utf32_stream );
	}
	return( -1 );
}

/* Calculates the name hash of an UTF-16 formatted string
 * Returns 1 if successful or -1 on error
 */
int libfsapfs_name_hash_calculate_from_utf16_string(
     uint32_t *name_hash,
     const uint16_t *utf16_string,
     size_t utf16_string_length,
     uint8_t use_case_folding,
     libcerror_error_t **error )
{
	uint8_t *utf32_stream                        = NULL;
	static char *function                        = "libfsapfs_name_hash_calculate_from_utf16_string";
	size_t utf16_string_index                    = 0;
	size_t utf32_stream_index                    = 0;
	size_t utf32_stream_size                     = 0;
	libuna_unicode_character_t unicode_character = 0;
	uint32_t calculated_checksum                 = 0;

	if( name_hash == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid name hash.",
		 function );

		return( -1 );
	}
	if( libuna_utf32_stream_size_from_utf16(
	     utf16_string,
	     utf16_string_length,
	     &utf32_stream_size,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
		 "%s: unable to retrieve UTF-32 stream size.",
		 function );

		goto on_error;
	}
	utf32_stream_size -= 4;

	utf32_stream = (uint8_t *) memory_allocate(
	                            sizeof( uint8_t ) * utf32_stream_size );

	if( utf32_stream == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_MEMORY,
		 LIBCERROR_MEMORY_ERROR_INSUFFICIENT,
		 "%s: unable to create UTF-32 stream.",
		 function );

		goto on_error;
	}
	while( utf16_string_index < utf16_string_length )
	{
		if( libuna_unicode_character_copy_from_utf16(
		     &unicode_character,
		     utf16_string,
		     utf16_string_length,
		     &utf16_string_index,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_CONVERSION,
			 LIBCERROR_CONVERSION_ERROR_INPUT_FAILED,
			 "%s: unable to copy Unicode character from UTF-16 string.",
			 function );

			goto on_error;
		}
/* TODO add NFD support */
		if( use_case_folding != 0 )
		{
/* TODO add case folding */
			unicode_character  = towlower( unicode_character );
		}
		if( libuna_unicode_character_copy_to_utf32_stream(
		     unicode_character,
		     utf32_stream,
		     utf32_stream_size,
		     &utf32_stream_index,
		     LIBUNA_ENDIAN_LITTLE,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_CONVERSION,
			 LIBCERROR_CONVERSION_ERROR_OUTPUT_FAILED,
			 "%s: unable to copy Unicode character to UTF-32 stream.",
			 function );

			goto on_error;
		}
		if( unicode_character == 0 )
		{
			break;
		}
	}
#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: UTF-32 stream data:\n",
		 function );
		libcnotify_print_data(
		 utf32_stream,
		 utf32_stream_size,
		 LIBCNOTIFY_PRINT_DATA_FLAG_GROUP_DATA );
	}
#endif
	if( libfsapfs_checksum_calculate_weak_crc32(
	     &calculated_checksum,
	     utf32_stream,
	     utf32_stream_size,
	     0xffffffffUL,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_SET_FAILED,
		 "%s: unable to calculate CRC-32.",
		 function );

		goto on_error;
	}
	memory_free(
	 utf32_stream );

	*name_hash = calculated_checksum & 0x003fffffUL;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: CRC-32 checkum\t\t: 0x%08" PRIx32 "\n",
		 function,
		 calculated_checksum );

		libcnotify_printf(
		 "%s: name hash\t\t: 0x%06" PRIx32 "\n",
		 function,
		 *name_hash );

		libcnotify_printf(
		 "\n" );
	}
#endif /* defined( HAVE_DEBUG_OUTPUT ) */

	return( 1 );

on_error:
	if( utf32_stream != NULL )
	{
		memory_free(
		 utf32_stream );
	}
	return( -1 );
}

