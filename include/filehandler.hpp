#ifndef FILEHANDLER_H_
#define FILEHANDLER_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vector>
#include <string>

class File
{
    public:
        using iterator = FILE*;
        // open new file
        explicit File(const std::string filename) : name{filename} {
            fh_ = fopen(name.c_str(), "r");
            if (fh_ == NULL) exit(EXIT_FAILURE);
        }
        // init file with existing open file and position
        explicit File(const int fileno, const int pos) {
            fh_ =  fdopen(fileno, "r");
            if (fh_ == NULL) exit(EXIT_FAILURE);
        }

        ~File() noexcept { if (fh_) fclose(fh_);}

        inline iterator fh() const noexcept {return fh_;}

        inline int tell() const noexcept {return ftell(fh_);}
        inline int seek(const int offset) {return fseek(fh_, offset, SEEK_SET);}
        inline int fnum() const noexcept {return fileno(fh_);}

    private:
        std::string name{};    
        iterator fh_{nullptr};
};

class FileIterator
{
    public:

        explicit FileIterator(const std::string filename) : file{filename} { }
        explicit FileIterator(const int fileno, const int pos) : file{fileno, pos} { }

        char* get_line();
        char* find_line(std::string key); 

        int grep(std::string key, size_t ilen, size_t ishift, std::vector<std::string>& vec);

        inline void rewind_fh() { rewind(file.fh()); };

        inline int tell() const noexcept {return file.tell();}
        inline int seek(const int offset) {return file.seek(offset);}

        File::iterator fh() const noexcept {return file.fh();}

        File f() noexcept {return file;}
    private:
        File file;
};


#endif
