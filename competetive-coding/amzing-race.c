// https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/algorithm/the-amazing-race-1/
// Populate Driver Height List
// Identify Vision Ahead
// Identify Vision following
// Calulate Sight
// Find Winner
#include <stdio.h>

#define NUMDRIVERS 10
int DriverHeight[NUMDRIVERS];
int DriverVision[NUMDRIVERS];
int winner = -1;

void PopulateDriverHeightList() {
    int i = 0;
    DriverHeight[i++] = 6;
    DriverHeight[i++] = 4;
    DriverHeight[i++] = 8;
    DriverHeight[i++] = 5;
    DriverHeight[i++] = 6;
    DriverHeight[i++] = 8;
    DriverHeight[i++] = 3;
    DriverHeight[i++] = 5;
    DriverHeight[i++] = 9;
    DriverHeight[i++] = 5;
}

void PrintDriverHeight(){
 for (int i = 0 ; i < NUMDRIVERS ; i++ ){
    printf("Driver Number: %d, Height: %d\n",i, DriverHeight[i] );
 } 
}

void initializeVision(){
    for (int i = 0 ; i < NUMDRIVERS ; i++ ){
        DriverVision[i] = 0;
    } 
 }

int getDriversAheadOfMe(int current_driver){
    int currentDriverHeight = DriverHeight[current_driver];
    int vision = 0;
    for ( int driver = current_driver -1 ; 
                driver >= 0 ; driver-- ) {
        vision++;
        int HieghtOfDriver = DriverHeight[driver];
        if ( HieghtOfDriver >= currentDriverHeight){
            break;
        }
    }
    return vision;
}

int getDriversBehindMe(int current_driver){
    int currentDriverHeight = DriverHeight[current_driver];
    int vision = 0;
    for ( int driver = current_driver + 1 ; 
                driver < NUMDRIVERS ; driver++ ) {
        vision++;
        int HieghtOfDriver = DriverHeight[driver];
        if ( HieghtOfDriver >= currentDriverHeight){
            break;
        }
    }
    return vision;
}

void SetVisionAhead(){
    for ( int current_driver = 1 ; current_driver < NUMDRIVERS ; current_driver++ ) {
        DriverVision[current_driver] = 
            DriverVision[current_driver] + 
            getDriversAheadOfMe(current_driver);
    }

}

void SetVisionBehind(){
    for ( int current_driver = 0 ; current_driver < NUMDRIVERS-1 ; current_driver++ ) {
        DriverVision[current_driver] = 
            DriverVision[current_driver] + 
            getDriversBehindMe(current_driver);
    }

}

void PrintDriverVision(){
 for (int i = 0 ; i < NUMDRIVERS ; i++ ){
    printf("Driver Number: %d, Vision: %d\n",i, DriverVision[i] );
 } 
}

void CalulateSight(){
 for (int i = 0 ; i < NUMDRIVERS ; i++ ){
    DriverVision[i] = DriverVision[i] * (i+1);
 } 
}

void PrintSight(){
 for (int i = 0 ; i < NUMDRIVERS ; i++ ){
    printf("Driver Number: %d, Sight: %d\n",i, DriverVision[i] );
 } 
}

void findWinner()
{
    int maxSight = -1;
    int maxSightIndex = -1;
    for (int driver = 0 ; driver < NUMDRIVERS ; driver++ ){
        int sight = DriverVision[driver];
        if (sight > maxSight ) {
            maxSight = sight;
            maxSightIndex = driver;
        }
    } 
    winner = maxSightIndex;
}

void printWinner()
{
    printf("Winner: %d\nHeight: %d\nSight: %d\n",
        winner+1,
         DriverHeight[winner], 
        DriverVision[winner] );
    
}

void main ()
{
    PopulateDriverHeightList();
    initializeVision();
    SetVisionAhead();
    SetVisionBehind();
    PrintDriverVision();
    CalulateSight();
    PrintSight();
    findWinner();
    printWinner();
}
