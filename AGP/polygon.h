//Fangshuo Li
//UNR CS302 FALL
//ART GALLERY PROBLEM

#pragma once
#include <vector>

//each point is a struct
struct Point
{
    //param ctor
    Point (float x = 0, float y = 0) : x(x), y(y), color(4) {}

    //xvalue
    float x;
    //yvalue
    float y;
    //color
    int color;
};

//each triangle is a struct
struct Triangle
{
    //param ctor
    Triangle (Point * point1, Point * point2, Point * point3) :
        p1(point1), p2(point2), p3(point3) {}

    //points stored as pointers for coloring purposes
    Point * p1;
    Point * p2;
    Point * p3;
};

//for better comprehension
using Polygon = std::vector<Point *>;
using Triangs = std::vector<Triangle>;

//necessary functions
Triangs triangulate (Polygon);
float crossProduct (const Point, const Point);
bool isClockwise (const Triangle);
bool pointInTriangle (Point * p, Triangle triangle);
bool hasPoint (Polygon polygon, Triangle triangle);

//color functions
int getLeastColor(Point * polyList[], Triangs t, int size);
int ColorFull (Triangle t);

//extra functions
// Point * copyOver (Polygon);
