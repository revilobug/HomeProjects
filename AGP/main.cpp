//Fangshuo Li
//UNR CS302 FALL
//ART GALLERY PROBLEM

#include <iostream>
#include <vector>
#include "polygon.h"

int main()
{
    std::cout << "========================================================================\n"
              << "How many points on the polygon?: "
              << std::endl;
    int counter;
    scanf("%i", &counter);

    Polygon poly;

    std::cout << "========================================================================\n"
              << "Enter points of polygon 1-by-1 and clockwise in 'x y' fashion as floats: "
              << std::endl;
    float xvalue;
    float yvalue;

    for (int i = 0; i < counter; i++)
    {
        scanf("%f %f", &xvalue, &yvalue);
        poly.push_back(new Point(xvalue, yvalue));
    }

    if (poly.size() < 3)
    {
        std::cout << "========================================================================\n"
                  << "Error: Enter polygon with at least 3 sides\n"
                  << "========================================================================"
                  << std::endl;
        return 0;
    }

    //this was the dataset used for testing
    // poly.push_back(new Point(7,5));
    // poly.push_back(new Point(6,4));
    // poly.push_back(new Point(7,3));
    // poly.push_back(new Point(6,0));
    // poly.push_back(new Point(5,1));
    // poly.push_back(new Point(3,0));
    // poly.push_back(new Point(1,1));

    //get size of the array
    int size = poly.size();
    //create list of pointers
    Point * pointList[poly.size()];

    //copy over the array into new array
    for (int i = 0; i <poly.size(); i++)
    {
        pointList[i] = poly[i];
    }

    //get the triangulations
    auto triangs = triangulate(poly);

    //print triangulation information
    std::cout << "========================================================================\n"
              << "Triangle Information\n"
              << "========================================================================"
              << std::endl;

    for (int i = 0; i < triangs.size(); i++)
    {
        std::cout << "Triangle Number: " << i << std::endl;
        std::cout << "Point 1: " << (triangs[i].p1) -> x << ", " << (triangs[i].p1) -> y << std::endl;
        std::cout << "Point 2: " << (triangs[i].p2) -> x << ", " << (triangs[i].p2) -> y << std::endl;
        std::cout << "Point 3: " << (triangs[i].p3) -> x << ", " << (triangs[i].p3) -> y << std::endl;
    }

    //get GuardCount using tri-coloring
    int guardCount = getLeastColor(pointList, triangs, size);

    //print color information
    std::cout << "========================================================================\n"
              << "The worst case number of guards is: " << guardCount << "\n"
              << "========================================================================"
              << std::endl;

    return 0;
}
