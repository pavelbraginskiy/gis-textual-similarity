#define BOOST_PYTHON_STATIC_LIB
#include <iostream>
#include <unordered_map>
#include <numeric>
#include <boost/python.hpp>
#include <boost/container_hash/hash.hpp>
#include <span>
using namespace boost::python;
constexpr int num_dimensions = 3;

typedef std::array<double, num_dimensions> point_t;
typedef std::span<point_t> trajectory_t;
typedef std::pair<trajectory_t, trajectory_t> args_t;
template <> struct std::hash<args_t>
{
	size_t operator()(const args_t &value) const noexcept
	{
		auto hash = boost::hash<trajectory_t::pointer>{}(value.first.data());
		boost::hash_combine(
			hash,
			boost::hash<trajectory_t::pointer>{}(value.second.data())
		);
		return hash;
	}
};
template <> struct std::equal_to<args_t>
{
	constexpr bool operator()(const args_t& lhs, const args_t& rhs) const
	{
		return
			lhs.first.data() == rhs.first.data() &&
			lhs.first.size() == rhs.first.size() &&
			lhs.second.data() == rhs.second.data() &&
			lhs.second.size() == rhs.second.size();
	}
};
typedef std::unordered_map<
	args_t,
	double
	> cache_t;

double dist(const point_t &a, const point_t &b)
{
	double dist_squared = 0;
	for (int i = 0; i < num_dimensions; ++i)
	{
		dist_squared += std::pow(a[i] - b[i], 2);
	}

	return std::sqrt(dist_squared);
}

point_t head(const trajectory_t t)
{
	return t[0];
}

trajectory_t rest(const trajectory_t t)
{
	return t.last(t.size() - 1);
}

double dtw(trajectory_t a, trajectory_t b, cache_t &cache)
{
	if (cache.contains({a, b}))
		return cache[{a,b}];

	double ret;

	if (a.size() == 0 && b.size() == 0)
	{
		ret = 0;
	}
	else if (a.size() == 0 || b.size() == 0)
	{
		ret = std::numeric_limits<double>::infinity();
	}
	else
	{
		ret = dist(head(a), head(b)) + std::min({
			dtw(a, rest(b), cache),
			dtw(rest(a), b, cache),
			dtw(rest(a), rest(b), cache)
		});
	}

	cache[{a, b}] = ret;

	return ret;
}

double erp(trajectory_t a, trajectory_t b, cache_t &cache)
{
	if (cache.contains({a, b}))
		return cache[{a,b}];

	static constexpr point_t g = {};

	double ret;

	if (b.size() == 0)
	{
		ret = 0;
		for (const auto &i : a)
		{
			ret += dist(i, g);
		}
	}
	else if (a.size() == 0)
	{
		ret = 0;
		for (const auto &i : b)
		{
			ret += dist(i, g);
		}
	}
	else
	{
		ret = std::min({
			erp(rest(a), rest(b), cache) + dist(head(a), head(b)),
			erp(rest(a), b, cache) + dist(head(a), g),
			erp(a, rest(b), cache) + dist(head(b), g)
		});
	}

	cache[{a, b}] = ret;

	return ret;
}

std::vector<point_t>* list_to_vec(const list &l)
{
	const auto ret = new std::vector<point_t>();
	const int length = len(l);
	ret->reserve(length);

	for (int i = 0; i < length; ++i)
	{
		list py_point = extract<list>(l[i]);
		point_t point;
		for (int j = 0; j < num_dimensions; ++j)
		{
			point[j] = extract<double>(py_point[j]);
		}
		ret->emplace_back(std::move(point));
	}

	return ret;
}

double dynamic_time_warping(list list_a, list list_b)
{
	const auto vec_a = list_to_vec(list_a);

	const auto vec_b = list_to_vec(list_b);

	auto cache = cache_t();

	const trajectory_t a = *vec_a;
	const trajectory_t b = *vec_b;

	const auto result = dtw(a, b, cache);

	delete vec_a;
	delete vec_b;

	return result;
}

double edit_distance_with_real_penalty(list list_a, list list_b)
{
	const auto vec_a = list_to_vec(list_a);
	const auto vec_b = list_to_vec(list_b);

	auto cache = cache_t();

	const trajectory_t a = *vec_a;
	const trajectory_t b = *vec_b;

	const auto result = erp(a, b, cache);

	delete vec_a;
	delete vec_b;

	return result;
}

BOOST_PYTHON_MODULE(TrajectoryDistance)
{
	using namespace boost::python;

	def("dtw", dynamic_time_warping);
	def("erp", edit_distance_with_real_penalty);

	scope current;
	current.attr("num_dimensions") = num_dimensions;
}