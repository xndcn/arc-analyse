#!/usr/bin/python2.7
import os, sys

class File:
    def __init__(self, img, abs_path, attribute, offset, size, link=None):
        self.img = img
        self.directory = os.path.dirname(abs_path)
        self.filename = os.path.basename(abs_path)
        self.attribute = attribute
        self.offset = offset
        self.size = size
        self.link = link
    
    def read_content(self):
        self.img.seek(self.offset)
        return self.img.read(self.size)
    
    def extract_content(self, output_directory):
        if output_directory[-1:] == '/':
            output_directory = output_directory[:-1]
            
        if not os.path.exists(output_directory + self.directory):
            os.makedirs(output_directory + self.directory)
        
        output_file = output_directory + self.directory + '/' + self.filename
        
        if self.link:
            os.symlink(output_directory + self.link, output_file)
        else:
            f = open(output_file, 'w')
            content = self.read_content()
            f.write(content)
            f.close()

class ImageParser:
    def __init__(self, img):
        self.img = file(img)
    
    @staticmethod
    def parse_string(img):
        string = ''
        while True:
            char = img.read(1)
            if char == '\0':
                break;
            string += char
        return string
    
    @staticmethod
    def skip_padding(img, align=4):
        offset = img.tell()
        skip = (align - (offset % align)) % align
        img.seek(offset + skip)
    
    @staticmethod
    def parse_uint32(img):
        bytes = [0]*4
        bytes[0] = ord(img.read(1))
        bytes[1] = ord(img.read(1))
        bytes[2] = ord(img.read(1))
        bytes[3] = ord(img.read(1))
        
        return (bytes[0]<<24) | (bytes[1]<<16) | (bytes[2]<<8) | (bytes[3]<<0)
    
    @staticmethod
    def parse_file(img):
        size = ImageParser.parse_uint32(img)
        attribute = ImageParser.parse_uint32(img)
        flag = ImageParser.parse_uint32(img)
        filepath = ImageParser.parse_string(img)
        link = ImageParser.parse_string(img) if flag == 0x0001 else None
        
        ImageParser.skip_padding(img)
        
        offset = ImageParser.parse_uint32(img)
        offset = offset - (size/0x10000)*0x10000
        
        return File(img, filepath, attribute, offset, size, link)

    def parse_header(self):
        self.img.seek(0)
        
        count = ImageParser.parse_uint32(self.img)
        unknown = ImageParser.parse_uint32(self.img)
        
        return count

    def parse(self):
        count = self.parse_header()
        files = [None] * count
        for i in xrange(count):
            files[i] = ImageParser.parse_file(self.img)
        
        return files
        
    def extract_all(self, output_directory):
        files = self.parse()
        for f in files:
            print 'extracting %s/%s...' % (f.directory, f.filename)
            f.extract_content(output_directory)
            
        print 'extracted %d files.' % len(files)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'fs-extract <fs.img> <output-directory>'
    else:
        parser = ImageParser(sys.argv[1])
        parser.extract_all(sys.argv[2])
