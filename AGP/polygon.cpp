//Fangshuo Li
//UNR CS302 FALL
//ART GALLERY PROBLEM

#include <iostream>
#include "polygon.h"

Triangs triangulate (Polygon polygon)
{
    //make copy of Polygon
    // Point * p = copyOver(polygon);

    Triangs complete;

    //while the polygon still has at least 3 sides
    while (polygon.size() >= 3)
    {
        //iterate through the polygon and try to triangulate with i, i+1, i+2
        for (int i = 0; i < polygon.size(); i++)
        {
            Point * point1 = polygon[i];
            Point * point2 = polygon[(i+1) % polygon.size()];
            Point * point3 = polygon[(i+2) % polygon.size()];

            //make temporary testing triangle with 3 points
            Triangle tempTriangle(point1, point2, point3);

            //if triangle will be outside of polygon
            //if counter-clockwise
            if (!(isClockwise(tempTriangle)))
            {
                // std::cout <<"here1" << "    iter: " << i << "   polySize: " << polygon.size()<<std::endl;
                continue;
            }

            //if there is a point of polygon that impedes into tempTriangle
            if (hasPoint (polygon, tempTriangle))
            {
                // std::cout <<"here1" << "    iter: " << i << "   polySize: " << polygon.size()<<std::endl;
                continue;
            }

            //add the triangle to the triangle array
            complete.emplace_back(tempTriangle);
            //remove the point from the polygon
            polygon.erase(std::begin(polygon) + (i+1) % polygon.size());
        }
    }

    return complete;
}

bool hasPoint (Polygon polygon, Triangle triangle)
{
    for (int i = 0; i < polygon.size(); i++)
    {
        //if the point is in the triangle
        if (pointInTriangle(polygon[i], triangle))
            //return that a point is in the triangle
            return true;
    }

    //means there is no point in the triangle
    return false;
}

//returning true means triangle is not valid
bool pointInTriangle (Point * p, Triangle triangle)
{
    bool isPointIn1, isPointIn2, isPointIn3;
    //if all three are clockwise means that there is a point in the triangle
    isPointIn1 = isClockwise(Triangle (p, triangle.p1, triangle.p2));
    isPointIn2 = isClockwise(Triangle (p, triangle.p2, triangle.p3));
    isPointIn3 = isClockwise(Triangle (p, triangle.p3, triangle.p1));
                // std::cout << p->x << p->y <<std::endl;
                // std::cout << isPointIn1 << isPointIn2 << isPointIn3 <<std::endl;

    //if all clockwise, then point is in triangle
    if (isPointIn1 && isPointIn2 && isPointIn3)
        return true;

    //if any is not clockwise, then point is not all in triangle
    else
        return false;
}

float isClockwiseHelper (const Point a, const Point b)
{
    //find determinant of the points
    float value = (a.x * b.y) - (a.y * b.x);
    return value;
}

bool isClockwise (const Triangle triangle)
{
    float sum = 0;
    //side 1
    sum += isClockwiseHelper(*(triangle.p1), *(triangle.p2));
    //side 2
    sum += isClockwiseHelper(*(triangle.p2), *(triangle.p3));
    //side 3
    sum += isClockwiseHelper(*(triangle.p3), *(triangle.p1));

    //std::cout << "sum: " << sum << std::endl;

    //if sum is less than 0 it is clockwise
    if (sum < 0)
    {
        return true;
    }
    //setting sum = 0 as counter-clockwise for simplicity
    else
        return false;
}

int getLeastColor(Point * polyList[], Triangs t, int size)
{
    bool allColorSet = false;

    //set initial colors
    //0 = red
    (t[0].p1) -> color = 0;
    //1 = blue
    (t[0].p2) -> color = 1;
    //2 = green
    (t[0].p3) -> color = 2;

    //while not all colors are set
    while (!allColorSet)
    {
        allColorSet = true;
        for (int i = 0; i < t.size(); i++)
        {
            //check if all colors are filled
            if (ColorFull(t[i]) == 3)
                continue;

            //if two colors are filled
            if (ColorFull(t[i]) == 2)
            {
                allColorSet = false;
                int missing = 7 - (t[i].p1) -> color - (t[i].p2) -> color - (t[i].p3) -> color;

                if ((t[i].p1) -> color == 4)
                    (t[i].p1) -> color = missing;

                else if ((t[i].p2) -> color == 4)
                    (t[i].p2) -> color = missing;

                else if ((t[i].p3) -> color == 4)
                    (t[i].p3) -> color = missing;
            }
        }
    }

    //initialize sums
    int redSum = 0, blueSum = 0, greenSum = 0;

    //iter through sums
    std::cout << "========================================================================\n"
              << "Point Color Information\n"
              << "========================================================================"
              << std::endl;

    for (int i = 0; i < size; i++)
    {
        //print out color information
        std::cout << "Point: " << i << "    Color:" << polyList[i] -> color << std::endl;

        //add to sum according to which color Point is
        if (polyList[i] -> color == 0)
            redSum++;

        if (polyList[i] -> color == 1)
            blueSum++;

        if (polyList[i] -> color == 2)
            greenSum++;
    }

    // std::cout << redSum << " " << blueSum << " " << greenSum << " "<< std::endl;

    //find the smallest of the three
    int smallest = 99999;

    if (redSum < smallest)
        smallest = redSum;
    if (blueSum < smallest)
        smallest = blueSum;
    if (greenSum < smallest)
        smallest = greenSum;

    return smallest;

}

int ColorFull (Triangle t)
{
    int sum = 0;
    //if color isn't the default color (4) then add one to sum
    if ((t.p1) -> color != 4)
        sum++;
    if ((t.p2) -> color != 4)
        sum++;
    if ((t.p3) -> color != 4)
        sum++;

    return sum;
}

// Point * copyOver (Polygon polygon)
// {
//     Point * pointList[polygon.size()];
//
//     for (int i = 0; i <polygon.size(); i++)
//     {
//         pointList[i] = polygon[i];
//     }
//
//     return pointList;
// }
