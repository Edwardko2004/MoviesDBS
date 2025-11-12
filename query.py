#
# CS 460: Problem Set 5: MongoDB Query Problems
#

#
# For each query, use a text editor to add the appropriate XQuery
# command between the triple quotes provided for that query's variable.
#
# For example, here is how you would include a query that finds
# the names of all movies in the database from 1990.
#
sample = """
    db.movies.find( { year: 1990 }, 
                    { name: 1, _id: 0 } )
"""

#
# 1. Put your query for this problem between the triple quotes found below.
#    Follow the same format as the model query shown above.
#
query1 = """
    
    db.people.find( { "name": { "$regex": "Joy", "$options": "i" } },  
                    { "name": 1, "dob": 1, "_id": 0 } )

"""

#
# 2. Put your query for this problem between the triple quotes found below.
#
query2 = """
    db.movies.find( { "name": { "$in": ["The Holdovers", "Spotlight"] } },  
                    { "name": 1, "runtime": 1, "_id": 0 } )
"""

#
# 3. Put your query for this problem between the triple quotes found below.
#
query3 = """
    db.movies.count( { "actors.name": "Robert Downey Jr.",  
    "earnings_rank": { "$exists": true } } )
"""

#
# 4. Put your query for this problem between the triple quotes found below.
#
query4 = """
    db.movies.aggregate([
  {
    $match: { "earnings_rank": { $lte: 200 } } // Match movies with an earnings_rank <= 200
  },
  {
    $group: {
      _id: "$rating",                         // Group by the rating field
      num_top_grossers: { $sum: 1 },          // Count the number of movies in each group
      best_rank: { $min: "$earnings_rank" }   // Find the smallest earnings_rank in each group
    }
  },
  {
    $project: {
      _id: 0,                                 // Exclude the _id field
      rating: "$_id",                         // Rename _id to rating
      num_top_grossers: 1,                    // Include num_top_grossers
      best_rank: 1                            // Include best_rank
    }
  }
])

"""

#
# 5. Put your query for this problem between the triple quotes found below.
#
query5 = """
   db.oscars.distinct(
  "movie.name",                           // Return distinct movie names
  {
    "year": { $gte: 2010, $lte: 2019 }   // Match Oscars awarded between 2010 and 2019
  }
)


"""

#
# 6. Put your query for this problem between the triple quotes found below.
#
query6 = """
    db.people.find(
  { "pob": { "$regex": "England, UK$" } }, // Match pob values ending with "England, UK"
  { "name": 1, "dob": 1, "pob": 1, "_id": 0 } // Include name, dob, and pob fields; exclude _id
)
.sort({ "dob": -1 }) // Sort by dob in descending order (youngest first)
.limit(3) // Limit the result to the top 3 documents

"""

#
# 7. Put your query for this problem between the triple quotes found below.
#
query7 = """
    db.movies.aggregate([
  {
    $match: {
      "earnings_rank": { $gte: 1, $lte: 15 },  // Filter for movies in the top 15 earnings
      "genre": { $regex: "A", $options: "i" }  // Filter for movies with "A" in the genre
    }
  },
  {
    $group: {
      _id: null,                               // Group all matching documents together
      num_action_in_top_15: { $sum: 1 },      // Count the number of matching movies
      avg_ranking: { $avg: "$earnings_rank" }, // Calculate the average earnings rank
      best_rank: { $min: "$earnings_rank" }    // Find the minimum (best) earnings rank
    }
  },
  {
    $project: {
      _id: 0,                                  // Exclude the _id field from the result
      num_action_in_top_15: 1,
      avg_ranking: 1,
      best_rank: 1
    }
  }
])

"""

#
# 8. Put your query for this problem between the triple quotes found below.
#
query8 = """
    db.movies.aggregate([
  {
    $match: {
      "genre": { $regex: "A", $options: "i" } // Match movies with "A" in their genre (action movies)
    }
  },
  {
    $unwind: "$directors"                    // Flatten the directors array to process each director separately
  },
  {
    $group: {
      _id: "$directors.name",                // Group by director's name
      num_action: { $sum: 1 }                // Count the number of action movies each director directed
    }
  },
  {
    $sort: {
      num_action: -1,                        // Sort by number of action movies (descending)
      _id: 1                                 // Sort alphabetically by director's name (ascending) as a tiebreaker
    }
  },
  {
    $limit: 3                                // Limit the results to the top 3 directors
  },
  {
    $project: {
      _id: 0,                                // Exclude the _id field
      director: "$_id",                      // Rename _id to director
      num_action: 1                          // Include num_action
    }
  }
])

"""

#
# 9. Put your query for this problem between the triple quotes found below.
#
query9 = """
    db.oscars.aggregate([
  {
    $match: {
      "type": { $ne: "BEST-PICTURE" }, // Exclude BEST-PICTURE awards
      "person.name": { $exists: true } // Ensure the award has an associated person
    }
  },
  {
    $group: {
      _id: "$person.name",           // Group by the person's name
      num_awards: { $sum: 1 },       // Count the total number of awards won by the person
      types: { $addToSet: "$type" }  // Create an array of unique award types
    }
  },
  {
    $match: {
      num_awards: { $gte: 3 }        // Filter to include only people who have won at least 3 awards
    }
  },
  {
    $sort: {
      num_awards: -1,                // Sort by number of awards in descending order
      _id: 1                         // Sort alphabetically by name in ascending order as a tiebreaker
    }
  },
  {
    $project: {
      _id: 0,                        // Exclude the _id field
      oscar_winner: "$_id",          // Rename _id to oscar_winner
      num_awards: 1,                 // Include num_awards
      types: 1                       // Include the array of unique award types
    }
  }
])

"""

#
# 10. Put your query for this problem between the triple quotes found below.
#
query10 = """
    db.movies.aggregate([
  {
    $unwind: "$actors"                  // Flatten the actors array to process each actor separately
  },
  {
    $group: {
      _id: "$actors.name",              // Group by actor's name
      movies: { $addToSet: "$name" },   // Create an array of unique movie names the actor appeared in
      first_appeared: { $min: "$year" }, // Find the earliest year the actor appeared in a movie
      last_appeared: { $max: "$year" },  // Find the latest year the actor appeared in a movie
      num_movies: { $sum: 1 }           // Count the number of movies the actor appeared in
    }
  },
  {
    $match: {
      num_movies: { $gte: 10 }          // Filter to include only actors who appeared in at least 10 movies
    }
  },
  {
    $project: {
      num_movies: 0                     // Remove the num_movies field
    }
  },
  {
    $project: {
      _id: 0,                           // Exclude the _id field
      actor: "$_id",                    // Rename _id to actor
      first_appeared: 1,                // Include first_appeared
      last_appeared: 1,                 // Include last_appeared
      movies: 1                         // Include the array of movies
    }
  },
  {
    $sort: {
      actor: 1                          // Sort by actor's name in alphabetical order
    }
  }
])

"""
