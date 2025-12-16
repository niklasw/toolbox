#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Polygon_with_holes_2.h>
#include <CGAL/Boolean_set_operations_2.h>
#include <vector>
#include <iostream>

typedef CGAL::Exact_predicates_exact_constructions_kernel K;
typedef CGAL::Polygon_2<K> Polygon_2;
typedef CGAL::Polygon_with_holes_2<K> Polygon_with_holes_2;
typedef std::vector<Polygon_with_holes_2> Polygon_with_holes_list;

int main() {
    Polygon_2 P, Q;
    P.push_back(K::Point_2(0, 0));
    P.push_back(K::Point_2(5, 0));
    P.push_back(K::Point_2(5, 5));
    P.push_back(K::Point_2(0, 5));

    Q.push_back(K::Point_2(1, 1));
    Q.push_back(K::Point_2(4, 1));
    Q.push_back(K::Point_2(4, 4));
    Q.push_back(K::Point_2(1, 4));

    Polygon_with_holes_list result;
    CGAL::difference(P, Q, std::back_inserter(result));

    // result now contains the polygons representing P - Q
    for (const auto& pwh : result) {
        std::cout << "Outer boundary:" << std::endl;
        for (auto it = pwh.outer_boundary().vertices_begin(); it != pwh.outer_boundary().vertices_end(); ++it) {
            std::cout << *it << std::endl;
        }

        for (auto hit = pwh.holes_begin(); hit != pwh.holes_end(); ++hit) {
            std::cout << "Hole:" << std::endl;
            for (auto it = hit->vertices_begin(); it != hit->vertices_end(); ++it) {
                std::cout << *it << std::endl;
            }
        }
        std::cout << "Polygon end" << std::endl;
    }
    return 0;
}

