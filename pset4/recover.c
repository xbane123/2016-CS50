#include <stdio.h>
#include <stdint.h>

int main(int argc, char* argv[])
{
    // check if only one command-line argument is applied
    if (argc != 2)
    {
        fprintf(stderr, "usage: ./recover filename\n");
        return 1;
    }
    
    // define input file
    char* infile = argv[1];
    
    // open input file
    FILE* memorycard = fopen(infile, "r");
    if (memorycard == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;        
    }
    
    // define JPEG block
    uint8_t buffer[512];

    // define the output file    
    FILE* img = NULL;
    
    // factor for the number of JPEGs 
    int counter = 0;
    
    // take 512 bytes every read til false
    //while(fread(buffer, sizeof(buffer), 1, memorycard)==1)    --- this way doesn't work well. I can't figure out why...sad...
    while (!feof(memorycard))
    {

        // check if reach the header of JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {   

            // close the existing output file
            if (img != NULL)
            {
                fclose(img);
            }
        
            // create filename for output file
            char filename[8];
            sprintf(filename, "%03d.jpg", counter);
            
            // open an output file
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fclose(memorycard);
                fclose(img);
                fprintf(stderr, "Could not create %s.\n", filename);
                return 3;        
            }                        

            // write to output file
            fwrite(buffer, sizeof(buffer), 1, img);

            // make counter ready for the next file
            counter++;
        }
        
        // this occurs when a JPEG is found and its first block is written
        else if (counter > 0) 
        {

            // write to output file
            fwrite(buffer, sizeof(buffer), 1, img);            
        }
        
        // this occurs when the first JPEG header is not reached yet
        //else  
        //{
            
            fread(buffer, sizeof(buffer), 1, memorycard);
            // mover infile pointer to next block
            //fseek(memorycard, sizeof(buffer), SEEK_CUR);
        //}
    }    

    // close input file
    fclose(memorycard);

    // close output file
    fclose(img);
    
    // the end
    return 0;
}
