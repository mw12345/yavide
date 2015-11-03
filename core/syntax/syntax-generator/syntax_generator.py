import sys
import shlex
import re
import logging
import os.path
from sets import Set
from subprocess import call

class SymbolDefinitionManager():
    def __init__(self, root_directory, tags_filename, tag_type, vim_keyword_type, out_filename):
        self.root_directory = root_directory
        self.tags_filename = tags_filename
        self.tag_type = tag_type
        self.vim_keyword_type = vim_keyword_type
        self.out_filename = out_filename

    def run(self):
        self.__generate_symbol_db()
        self.__extract()
        self.__generate_vim_syntax_file()

    def __extract(self):
        if os.path.exists(self.tags_filename):
            with open(self.tags_filename) as f:
                lines = f.readlines()
                symbol = Set()
                for l in lines:
                    if not l.startswith("!_TAG_"): # ignore the ctags tag file information
                        #if not "access:private" in l: # only take into account tags which are not declared as private/protected
                        #    if not "access:protected" in l:
                        #        if not "~" in l[0][0]: # we don't want destructors to be in the list
                        symbol.add(re.split(r'\t+', l)[0])
                out = open(self.out_filename, "w")
                out.write("\n".join(symbol))
        else:
            logging.error("Non-existing filename or directory '{0}'.".format(filename))

    def __generate_symbol_db(self):
        if os.path.exists(self.root_directory):
            cmd  = 'ctags --languages=C++ --fields=a --extra=-fq ' + '--c++-kinds=' + self.tag_type  + ' -f ' + self.tags_filename + ' -R ' + self.root_directory
            logging.info("Generating the db: '{0}'".format(cmd))
            call(shlex.split(cmd))
        else:
            logging.error("Non-existing directory '{0}'.".format(directory))
   
    def __generate_vim_syntax_file(self):
        with open(self.out_filename) as f:
            syntax_element = []
            lines = f.readlines()
            for l in lines:
                element = "syntax keyword " + self.vim_keyword_type + " " + l
                syntax_element.append(element)
            generated_syntax_file = self.tags_filename + ".vim"
            out = open(generated_syntax_file, "w")
            out.writelines(syntax_element)
                            
class NamespaceDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-namespace", "n", "yavideCppNamespace", "tags-namespace-processed")

class ClassDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-class", "c", "yavideCppClass", "tags-class-processed")

class StructDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-struct", "s", "yavideCppStructure", "tags-struct-processed")

class EnumDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-enum", "g", "yavideCppEnum", "tags-enum-processed")

class EnumValueManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-enum-value", "e", "yavideCppEnumValue", "tags-enum-value-processed")

class UnionDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-union", "u", "yavideCppUnion", "tags-union-processed")

class ClassStructUnionMemberDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-class-struct-union-member", "m", "yavideCppClassStructUnionMember", "tags-class-struct-union-member-processed")

class LocalVariableDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-local-variable", "l", "yavideCppLocalVariable", "tags-local-variable-processed")

class VariableDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-variable", "v", "yavideCppVariableDefinition", "tags-variable-processed")

class FuncPrototypeManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-func-proto", "p", "yavideCppFunctionPrototype", "tags-func-proto-processed")

class FuncDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-func", "f", "yavideCppFunctionDefinition", "tags-func-processed")

class MacroDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-macro", "d", "yavideCppMacro", "tags-macro-processed")

class TypedefDefinitionManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-typedef", "t", "yavideCppTypedef", "tags-typedef-processed")

class ExternForwardDeclarationManager(SymbolDefinitionManager):
    def __init__(self, root_directory):
        SymbolDefinitionManager.__init__(self, root_directory, "/tmp/tags-extern-fwd", "x", "yavideCppExternForwardDeclaration", "tags-extern-fwd-processed")

def main():
    if len(sys.argv) == 2:
        logging.info("Starting symbol generator for sources found at '{0}' ...".format(sys.argv[1]))
        symbolTypeList = [
            NamespaceDefinitionManager(sys.argv[1]), 
            ClassDefinitionManager(sys.argv[1]), 
            StructDefinitionManager(sys.argv[1]),
            EnumDefinitionManager(sys.argv[1]),
            EnumValueManager(sys.argv[1]),
            UnionDefinitionManager(sys.argv[1]),
            ClassStructUnionMemberDefinitionManager(sys.argv[1]),
            LocalVariableDefinitionManager(sys.argv[1]),
            VariableDefinitionManager(sys.argv[1]),
            FuncPrototypeManager(sys.argv[1]),
            FuncDefinitionManager(sys.argv[1]),
            MacroDefinitionManager(sys.argv[1]), 
            TypedefDefinitionManager(sys.argv[1]),
            ExternForwardDeclarationManager(sys.argv[1])
        ]

        for symbol in symbolTypeList:
            symbol.run()
        
    else:
        logging.error('Insufficient number of arguments. Please provide a directory containing sources to generate symbols for.')

if __name__ == "__main__":
    main()

