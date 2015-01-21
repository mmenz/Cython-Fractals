//
// Fractal.c
// Fractal generator
//   Fractal [Equation] [x0] [y0] [x1] [y1]
// Michael Menz
//

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>

int MAP_SIZE;
int MAP_WIDTH;
int MAP_HEIGHT;

int diverge_max = 0;
int diverge_min = 10000;

char MAX(int x, int y){
  if (x > y)
    return x;
  return y;
}

int normalize(int value){
    if (diverge_max == 0)
      return 0;
    int rv = (value - diverge_min) * 256 / diverge_max;
    if (rv > 255)
      return 255;
    if (rv < 0)
      return 0;
    return rv;
}

int squareJulia(double x0, double y0, double x1, double y1,
                  double realC, double imagC, int iters,
                  int i){
  int count = 0;
  double real = (double)(i%MAP_WIDTH) / MAP_WIDTH * (x1 - x0) + x0;
  double imag = (double)(i/MAP_WIDTH) / MAP_HEIGHT * (y1 - y0) + y0;
  complex double z = real + imag*I;
  complex double c = realC + imagC*I;
  for (int iter = 0; iter < iters; iter++){
    if (cabs(z) > 10000000){
      count++;
    }
    else{
      z = z*z + c;
    }
  }
  return count;
}

int expJulia(double x0, double y0, double x1, double y1,
                  double realC, double imagC, int iters,
                  int i){
  int count = 0;
  double real = (double)(i%MAP_WIDTH) / MAP_WIDTH * (x1 - x0) + x0;
  double imag = (double)(i/MAP_WIDTH) / MAP_HEIGHT * (y1 - y0) + y0;
  complex double z = real + imag*I;
  complex double c = realC + imagC*I;
  for (int iter = 0; iter < iters; iter++){
    if (cabs(z) > 10000000){
      count = iters - iter;
      return count;
    }
    else{
      z = cexp(z) + c;
    }
  }
  return count;
}

int squareLogJulia(double x0, double y0, double x1, double y1,
                  double realC, double imagC, int iters,
                  int i){
  int count = 0;
  double real = (double)(i%MAP_WIDTH) / MAP_WIDTH * (x1 - x0) + x0;
  double imag = (double)(i/MAP_WIDTH) / MAP_HEIGHT * (y1 - y0) + y0;
  complex double z = real + imag*I;
  complex double c = realC + imagC*I;
  for (int iter = 0; iter < iters; iter++){
    if (cabs(z) > 10000000){
      count++;
    }
    else{
      z = (z*z+z)/(clog(z)) + c;
    }
  }
  return count;
}



int mandelbrot(double x0, double y0, double x1, double y1,
                  double realC, double imagC, int iters,
                  int i){
  int count = 0;
  double real = (double)(i%MAP_WIDTH) / MAP_WIDTH * (x1 - x0) + x0;
  double imag = (double)(i/MAP_WIDTH) / MAP_HEIGHT * (y1 - y0) + y0;
  complex double z = 0 + 0*I;
  complex double c = real + imag*I;
  for (int iter = 0; iter < iters; iter++){
    if (cabs(z) > 10000000){
      count++;
    }
    else{
      z = cpow(z, 2) + c;
    }
  }
  return count;
}


void testSimple(double x0, double y0, double x1, double y1, int *dmap){
  for (int i =0; i < MAP_SIZE; i++){
    dmap[i] = i%10;
  }
}

void approximateMinMax(double x0, double y0, double x1, double y1,
                       double realC, double imagC, int iters){
  int min = iters;
  int max = 0;
  for (int j = 0; j < MAP_SIZE; j+=10){
    int count = expJulia(x0, y0, x1, y1, realC, imagC, iters, j);
    if (count < min)
      min = count;
    if (count > max)
      max = count;
  }
  if (max > diverge_max)
    diverge_max = max;
  if (min < diverge_min)
    diverge_min = min;
}

void writeFractalToFile(double x0, double y0, double x1, double y1,
                        double realC, double imagC, int iters,
                        char* name, int *colormap){
  FILE* fp = fopen(name, "wb");
  fprintf(fp, "P6\n%d %d\n255\n", MAP_WIDTH, MAP_HEIGHT);
  for (int i = 0; i < MAP_SIZE; i++){
    int count = normalize(expJulia(x0, y0, x1, y1, realC, imagC, iters, i));
    char color[3];
    color[0] = colormap[count];
    color[1] = colormap[count+256];
    color[2] = colormap[count+512];
    fwrite(color, 1, 3, fp);
  }
  fclose(fp);
  printf("Wrote ppm to file\n");
}

int main(int argc, char* argv[]){

  if (argc != 11){
    return 1;
  }

  int frames = atoi(argv[1]);

  double x0;
  double y0;
  double x1;
  double y1;

  sscanf(argv[2], "%lf", &x0);
  sscanf(argv[3], "%lf", &y0);
  sscanf(argv[4], "%lf", &x1);
  sscanf(argv[5], "%lf", &y1);

  printf("%f %f %f %f\n", x0, y0, x1, y1);

  double realC;
  double imagC;

  sscanf(argv[6], "%lf", &realC);
  sscanf(argv[7], "%lf", &imagC);

  int iters;
  iters = atoi(argv[8]);

  MAP_WIDTH = atoi(argv[9]);
  MAP_HEIGHT = atoi(argv[10]);
  MAP_SIZE = MAP_WIDTH * MAP_HEIGHT;

  int colormap[3*256];

  // read in colormap from color.col file
  FILE *fp;
  fp = fopen("color.col", "r");
  for (int i=0; i<3*256; i++){
    int x;
    fscanf(fp, "%d", &x);
    colormap[i] = x;
  }
  fclose(fp);

  for (int i = 0; i < frames; i++){
    approximateMinMax(x0, y0, x1, y1, -1+0.001*i, imagC, iters);
  }
  for (int j = 0; j < frames; j++){
    char name[] = "video/test00000.ppm";
    int num = j;
    for (int k = 0; k < 5; k++){
      name[14-k] = num%10 + 48;
      num = num /10;
    }
    writeFractalToFile(x0, y0, x1, y1, -1 + 0.001*j, imagC, iters, name, colormap);
  }
}
