#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char *argv[])
{
	// Variables
	MPI_Status status;
	double t1, t2, t;
	int rank, size;
	void* buffer;
	int i, j, step, max, rep;

	step = 100000;
	max  = 1000000;
	rep  = 100;

	// Initialize MPI
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);

	// Compute the ping value
	for (i = 0; i < max; i += step) {
		buffer = malloc(i);
		// Compute average ping for REP iterations
		t = 0.0;
		for (j = 0; j < rep; j++) {
			if (rank == 0) {
				t1 = MPI_Wtime();
				MPI_Send(buffer, i, MPI_BYTE, 1, 0, MPI_COMM_WORLD);
				MPI_Recv(buffer, i, MPI_BYTE, 1, 1, MPI_COMM_WORLD, &status);
				t2 = MPI_Wtime();
				t += t2 - t1;
			} else if (rank == 1) {
				MPI_Recv(buffer, i, MPI_BYTE, 0, 0, MPI_COMM_WORLD, &status);
				MPI_Send(buffer, i, MPI_BYTE, 0, 1, MPI_COMM_WORLD);
			}
		}
		// Print each independent result
		if (rank == 0) {
			t /= rep;
			t /= 2;
			t *= 1e6;
			printf("Time for %d bytes is %5.3f\n", i, t);
		}
		free(buffer);
	}

	// Finalize MPI
	MPI_Finalize();
	return 0;
}
