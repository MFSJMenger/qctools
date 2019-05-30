#include "filehandler.hpp"


char* 
FileIterator::get_line()
{
    char* line = nullptr;
    size_t len;
    ssize_t read = getline(&line, &len, file.fh()); 
    if (read == -1) {
        return nullptr; 
    }
    return line;
};

char* 
FileIterator::find_line(std::string key) {
    char * line = nullptr;
    const char * ref = key.c_str();
    while (true) {
        line = get_line();
        if (line == nullptr) { break; }
        if (strstr(line, ref) != NULL) {
            break;
        }
    }
    return line;
};

int 
FileIterator::grep(std::string key, size_t ilen, size_t ishift, std::vector<std::string>& vec) 
{
    char* line = find_line(key);
    if (line == nullptr) {
        return -1;
    }
    if (ishift == 0) {
       ilen = ilen - 1;
       vec.push_back(std::string{line}); 
    } else if (ishift > 0) {
        for(size_t i=1; i<ishift; ++i) {
            line = get_line();
            if (line == nullptr) {
                return -1;
            }
        }
    }

    for (size_t i=0; i<ilen; ++i) {
        line = get_line();
        if (line == nullptr) {
            return 0;
        }
        vec.push_back(std::string{line});
    }
    return 1;
};
