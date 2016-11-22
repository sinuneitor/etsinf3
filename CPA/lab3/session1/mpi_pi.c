#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <math.h>

int main(int argc, char *argv[])
{
	int n, myid, numprocs, i;
	double mypi, pi, h, sum, x;
	MPI_Status status;

	// Initialize MPI
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
	MPI_Comm_rank(MPI_COMM_WORLD, &myid);

	if (argc == 2) n = atoi(argv[1]);
	else n = 100;
	
	if (n <= 0) MPI_Abort(MPI_COMM_WORLD, MPI_ERR_ARG);

	// Computation
	h 	= 1.0 / (double) n;
	sum = 0.0;
	for (i = myid + 1; i <= n; i += numprocs) {
		x = h * ((double) i - 0.5);
		sum += (4.0 / (1.0 + x * x));
	}
	mypi = h * sum;

	// Reduction
	if (myid == 0) {
		pi = mypi;
		for (i = 1; i < numprocs; i++) {
			MPI_Recv(&mypi, 1, MPI_DOUBLE, i, 0, MPI_COMM_WORLD, &status);
			pi += mypi;
		}
	} else {
		MPI_Send(&mypi, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
	}

	// Print result
	if (myid == 0) {
		printf("Computation of PI with %d processes\n", numprocs);
		printf("With %d intervals, PI is approximately %.16f (error = %.16f)\n", n, pi, fabs(pi-M_PI));
	}

	// Finalize MPI
	MPI_Finalize();
	return 0;
}

