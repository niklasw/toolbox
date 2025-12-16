#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Polygon_with_holes_2.h>
#include <CGAL/Boolean_set_operations_2.h>
#include <CGAL/Constrained_Delaunay_triangulation_2.h>
#include <CGAL/Constrained_triangulation_plus_2.h>
#include <vector>
#include <iostream>
#include <string>
#include <boost/algorithm/string.hpp>

typedef CGAL::Exact_predicates_exact_constructions_kernel K;
typedef CGAL::Polygon_2<K> Polygon_2;
typedef CGAL::Polygon_with_holes_2<K> Polygon_with_holes_2;
typedef CGAL::General_polygon_with_holes_2<K> General_polygon_with_holes_2;
typedef std::vector<Polygon_with_holes_2> Polygon_with_holes_list;

typedef CGAL::Triangulation_vertex_base_2<K> Vb;
typedef CGAL::Constrained_triangulation_face_base_2<K> Fb;
typedef CGAL::Triangulation_data_structure_2<Vb, Fb> Tds;
typedef CGAL::Exact_predicates_tag Itag;
typedef CGAL::Constrained_Delaunay_triangulation_2<K, Tds, Itag> CDT;
typedef CGAL::Constrained_triangulation_plus_2<CDT> CDTP;


std::string split_string(const std::string& s, const std::string& delimiter, int index) {
    std::vector<std::string> tokens;
    boost::split(tokens, s, boost::is_any_of(delimiter));
    return tokens[index];
}

std::string join_string(const std::vector<std::string>& tokens, const std::string delimiter=" ") {
    return boost::algorithm::join(tokens, delimiter);
}

bool is_point_inside_polygon(const K::Point_2& point, const Polygon_2& polygon) {
    return polygon.bounded_side(point) == CGAL::ON_BOUNDED_SIDE;
}


bool is_point_inside_holes(const K::Point_2& point, const Polygon_with_holes_2& pwh) {
    for (auto hit = pwh.holes_begin(); hit != pwh.holes_end(); ++hit) {
        if (is_point_inside_polygon(point, *hit)) {
            return true;
        }
    }
    return false;
}


std::vector<CDT::Triangle> get_triangles_from_triangulation(const CDTP& cdt, const Polygon_with_holes_2& pwh) {
    std::vector<CDT::Triangle> triangles;

    const Polygon_2& outer = pwh.outer_boundary();
    for (auto fit = cdt.finite_faces_begin(); fit != cdt.finite_faces_end(); ++fit) {
        auto triangle = cdt.triangle(fit);
        K::Point_2 circumcenter = CGAL::circumcenter(triangle);

        if (is_point_inside_polygon(circumcenter, outer) && !is_point_inside_holes(circumcenter, pwh)) {
            triangles.push_back(triangle);
        }
    }

    return triangles;
}


CDTP triangulate_polygon_with_holes(const Polygon_with_holes_2& pwh) {
    CDTP cdt;

    // Insert outer boundary
    const Polygon_2& outer = pwh.outer_boundary();
    cdt.insert_constraint(outer.vertices_begin(), outer.vertices_end());

    // Insert holes
    for (auto hit = pwh.holes_begin(); hit != pwh.holes_end(); ++hit) {
        const Polygon_2& hole = *hit;
        cdt.insert_constraint(hole.vertices_begin(), hole.vertices_end());
    }
    return cdt;
}


void triangulation_to_obj(const CDTP& cdt, const std::string& filename) {
    std::ofstream out(filename);
    // Output the triangles
    for (auto it = cdt.finite_faces_begin(); it != cdt.finite_faces_end(); ++it) {
        for (int i=0; i<3; i++) {
            const auto& p = cdt.triangle(it)[i];
            out << "v " << p.x() << " " << p.y() << " 0" << std::endl;
        }
    }

    std::string surface_name = split_string(filename, ".", 0);

    out << "g " << surface_name << std::endl;

    int i = 1;
    for (auto it = cdt.finite_faces_begin(); it != cdt.finite_faces_end(); ++it) {
        out << "f " << i << " " << i+1 << " " << i+2 << std::endl;
        i += 3;
    }
    out.close();
}


int main() {
    Polygon_2 P, Q, R;
    P.push_back(K::Point_2(0, 0));
    P.push_back(K::Point_2(5, 0));
    P.push_back(K::Point_2(5, 5));
    P.push_back(K::Point_2(0, 5));

    Q.push_back(K::Point_2(1, 1));
    Q.push_back(K::Point_2(4, 1));
    Q.push_back(K::Point_2(4, 4));
    Q.push_back(K::Point_2(1, 4));


    // Add another hole for demonstration
    Q.push_back(K::Point_2(2, 2));
    Q.push_back(K::Point_2(4.0, 2));
    Q.push_back(K::Point_2(4.0, 3));
    Q.push_back(K::Point_2(2, 3));

    std::vector<Polygon_2> hole_polygons;
    hole_polygons.push_back(Q);
    hole_polygons.push_back(R);

    Polygon_with_holes_list diff_result;
    Polygon_with_holes_list union_result;

    CGAL::difference(P, Q, std::back_inserter(diff_result));

    std::cout << "Number of polygons after difference: " << diff_result.size() << std::endl;

    // CGAL::join(diff_result.begin(), diff_result.end(), std::back_inserter(union_result));   

    const Polygon_with_holes_2& pwh = diff_result[0];

    // CGAL::difference(pwh, R, std::back_inserter(diff_result));

    int fcount = 0;
    for (const auto& pwh : diff_result) {
        std::string filename = "output_" + std::to_string(fcount) + ".obj";
        triangulation_to_obj(triangulate_polygon_with_holes(pwh), filename);
        fcount++;
    }

    /*
    Polygon_with_holes_list diff_result;
    diff_result.push_back(Polygon_with_holes_2(P));

    for (const auto& hole: hole_polygons) {
        Polygon_with_holes_list temp_result;
        for (const auto& pwh : diff_result) {
            CGAL::difference(pwh, hole, std::back_inserter(temp_result));
        }
        diff_result = std::move(temp_result);        
    }

    std::cout << "Number of polygons after difference: " << diff_result.size() << std::endl;

    // Triangulate the resulting polygons
    for (const auto& pwh : diff_result) {
         triangulation_to_obj(triangulate_polygon_with_holes(pwh));
    }
    */

    return 0;
}

