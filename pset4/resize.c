/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    int n=atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    // create outfile's BITMAPFILEHEADER
    BITMAPFILEHEADER bfout;
    bfout = bf;
    
    // create outfile's BITMAPINFOHEADER
    BITMAPINFOHEADER biout;
    biout = bi;

    biout.biWidth=bi.biWidth*n;
    biout.biHeight=bi.biHeight*n; 
    biout.biSizeImage=((3*bi.biWidth*n)+(4-(bi.biWidth*n*3)%4)%4)*abs(bi.biHeight*n);
    bfout.bfSize=biout.biSizeImage+54;      

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfout, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biout, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    // determine padding for infile
    int in_padding =  (4 - (bi.biWidth*sizeof(RGBTRIPLE)) % 4) % 4;

    // determine padding for outfile
    int out_padding =  (4 - (bi.biWidth*n*sizeof(RGBTRIPLE)) % 4) % 4;

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // temporary storage
        RGBTRIPLE triple;

        // copy n times vertically
        for (int y = 0; y < n; y++)
        {
            fseek(inptr, 54+(bi.biWidth*3+in_padding)*i, SEEK_SET);
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // horizontal * n-1
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);  
                for (int x = 0; x < n-1; x++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
                // horizontal * nth
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }

            // then add it back (to demonstrate how)
            for (int k = 0; k < out_padding; k++)
            {
               fputc(0x00, outptr);
            }
        }

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
