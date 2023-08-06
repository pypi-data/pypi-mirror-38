#include <string.h>
#include <stdlib.h>
#include "Python.h"
// Includes all needed stuff.

typedef struct {
    char* ParsingString;
    int IgnoreQuotes;
    int HitAllArgs;
    char* LastParse;
} ArgParserStructure;
// The structure for the argument parser.

static ArgParserStructure ArgParser_Next(ArgParserStructure structure) {
    char Quote = '"';
    // Defines a quote.

    char Space = ' ';
    // Defines a space.

    if (strcmp(structure.ParsingString, "") == 0) {
        structure.HitAllArgs = 1;
        return structure;
    }
    // Returns if all arguments have been hit.

    int InQuotes = 0;
    // Sets if the parser is inside quotes.

    int ParsingStringLength = (int)strlen(structure.ParsingString);
    char* CurrentParse = PyMem_Calloc(ParsingStringLength, 1);
    // Defines the current parse.

    char* *parsing_str = &structure.ParsingString;
    char current_char = *parsing_str[0];
    while (current_char != '\0') {
        if (current_char == Quote) {
            // This is a quote.
            if (InQuotes == 1) {
                // This is the end of some quoted text.
                ++*parsing_str;
                structure.LastParse = CurrentParse;
                return structure;
            } else {
                // How do we handle the quote?
                if (structure.IgnoreQuotes) {
                    CurrentParse[(int) strlen(CurrentParse)] = current_char;
                } else {
                    InQuotes = 1;
                }
            }
        } else if (current_char == Space) {
            // This is a space.
            if (InQuotes == 0) {
                // Probably count this as a break.
                if (!(strcmp(CurrentParse, "") == 0)) {
                    ++*parsing_str;
                    structure.LastParse = CurrentParse;
                    return structure;
                }
            } else {
                // Add this to the quote text.
                CurrentParse[(int) strlen(CurrentParse)] = current_char;
            }
        } else {
            // Add this to the text.
            CurrentParse[(int) strlen(CurrentParse)] = current_char;
        }

        ++*parsing_str;
        current_char = *parsing_str[0];
        // Knocks off a character.
    }

    structure.ParsingString = "";
    structure.LastParse = CurrentParse;
    return structure;
    // All args done! Lets return the structure.
}
// Gets the next argument.
