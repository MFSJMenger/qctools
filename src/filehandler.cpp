#include "filehandler.hpp"


inline
bool
is_str_substring(const char* substring, const char* string) 
{
    return strstr(string, substring) != NULL; 
};


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
FileIterator::find_line(const std::string& key) {
    const char * ref = key.c_str();
    char * line = nullptr;

    while (true) {
        line = get_line();
        if (line == nullptr)  break; 
        if (is_str_substring(ref, line)) break; 
    }
    return line;
};

std::vector<std::string>
FileIterator::in_between(const std::string& start, const std::string& end, int& ierr) 
{
    // reserve memory for output string
    std::vector<std::string> vec;
    vec.reserve(100);               // reserve 100 lines
    const char* cend = end.c_str();
    //
    ierr = 1;
    //
    char* line = find_line(start);
    if (line == nullptr) {
        // did not find line
        ierr = -1;
        return vec;
    }
    //
    vec.push_back(std::string{line});
    while(!is_str_substring(cend, line)) {
            line = get_line();
            if (line == nullptr) {
                ierr = 0;
                return vec;
            }
            vec.push_back(std::string{line});
    }; 
    // 
    return vec;
};

std::vector<std::string>
FileIterator::till(const std::string& end, int& ierr) 
{
    // reserve memory for output string
    std::vector<std::string> vec;
    vec.reserve(100);               // reserve 100 lines
    const char* cend = end.c_str();
    //
    ierr = 1;
    //
    char* line = get_line();
    if (line == nullptr) {
        // did not find line
        ierr = -1;
        return vec;
    }
    //
    vec.push_back(std::string{line});
    while(!is_str_substring(cend, line)) {
            line = get_line();
            if (line == nullptr) {
                ierr = 0;
                return vec;
            }
            vec.push_back(std::string{line});
    }; 
    // 
    return vec;
};


std::vector<std::string>
FileIterator::grep(const std::string& key, size_t ilen, 
                   const size_t ishift, int& ierr) 
{
    //
    ierr = 1;
    // reserve memory for output string
    std::vector<std::string> vec;
    vec.reserve(ilen);
    // find keyword
    char* line = find_line(key);
    // go-on
    if (line == nullptr) {
        ierr = -1;
        return vec;
    }
    // shift 
    if (ishift == 0) {
       ilen = ilen - 1;
       vec.push_back(std::string{line}); 
    } else if (ishift > 0) {
        for(size_t i=1; i<ishift; ++i) {
            line = get_line();
            if (line == nullptr) {
                ierr = -1;
                return vec;
            }
        }
    }
    // push 
    for (size_t i=0; i<ilen; ++i) {
        line = get_line();
        if (line == nullptr) {
            ierr = 0;
            return vec;
        }
        vec.push_back(std::string{line});
    }
    //
    return vec;
};
