from enum import Enum
import struct

class ElfHeaderIdent(object):
	ei_class_dict = {0:"Invalid class", 1:"32-bit objects", 2:"64-bit objects"}
	ei_class = 0

	ei_data_dict = {0:"Invalid data encoding", 1:"LSB", 2:"MSB"}
	ei_data = 0

	#EI_VERSION
	ei_version = 0
	
	@staticmethod
	def parse(header_ident):
		ident = ElfHeaderIdent();
		if (ord(header_ident[0]) == 0x7f) and (header_ident[1] == ('E')) and (header_ident[2] == ('L')) and (header_ident[3] == ('F')):
			ident.ei_class = header_ident[4]
			ident.ei_data = header_ident[5]
			ident.ei_version = header_ident[6]
			return ident
		else:
			return None
	pass

class ElfHeader(object):
	e_type_dict = {0:"No file type", 1:"Relocatable file", 2:"Executable file", 3:"Shared object file", 4:"Core file"}
	e_machine_dict = {0: "No machine", 1:"AT&T WE 32100", 2:"SPARC", 3:"Intel Architecture", 4:"Motorola 68000", 5:"Motorola 88000", 7:"Intel 80860", 8:"MIPS RS3000 Big-Endian", 9:"MIPS RS4000 Big-Endian"}
	e_version_dict = {0:"Invalid version", 1:"Current version"}


	e_ident = ElfHeaderIdent()
	e_type = 0
	e_machine = 0
	e_version = 0
	e_entry = 0
	e_phoff = 0
	e_shoff = 0
	e_flags = 0
	e_ehsize = 0
	e_phentsize = 0
	e_phnum = 0
	e_shentsize = 0
	e_shnum = 0
	e_shstrndx = 0


	@staticmethod
	def parse(header):
		elf_header = ElfHeader()
		elf_header.e_ident = ElfHeaderIdent.parse(header[0:16])
		
		if(elf_header.e_ident == None):
			return None
		
		elf_header.e_type, elf_header.e_machine, elf_header.e_version, elf_header.e_entry, elf_header.e_phoff = struct.unpack("2H3I", header[16:32])
		elf_header.e_shoff, elf_header.e_flags, elf_header.e_ehsize, elf_header.e_phentsize, elf_header.e_phnum = struct.unpack("2I3H", header[32:46])
		elf_header.e_shentsize, elf_header.e_shnum, elf_header.e_shstrndx = struct.unpack("3H", header[46:52])
		return elf_header
	pass
