db = db.getSiblingDB("netflix_catalog");

db.movies.createIndex({ title: 1 });
db.movies.createIndex({ genres: 1 });
db.movies.createIndex({ "cast.name": 1 });

db.movies.insertMany([
  {
    title: "Inception",
    content_type: "movie",
    year: 2010,
    duration_mins: 148,
    rating: "PG-13",
    imdb_score: 8.8,
    genres: ["sci-fi", "thriller", "action"],
    cast: [
      { name: "Leonardo DiCaprio", role: "Cobb" },
      { name: "Elliot Page",       role: "Ariadne" }
    ],
    streaming_urls: {
      hd:  "s3://netflix-content/inception/hd.m3u8",
      uhd: "s3://netflix-content/inception/4k.m3u8"
    },
    languages: ["en", "fr", "de"],
    subtitles: ["en", "fr", "de", "ja", "ko"]
  },
  {
    title: "Stranger Things",
    content_type: "series",
    year: 2016,
    rating: "TV-14",
    imdb_score: 8.7,
    genres: ["sci-fi", "horror", "drama"],
    cast: [
      { name: "Winona Ryder",   role: "Joyce Byers" },
      { name: "David Harbour",  role: "Jim Hopper" }
    ],
    seasons: [
      { season: 1, episodes: 8, year: 2016 },
      { season: 2, episodes: 9, year: 2017 },
      { season: 3, episodes: 8, year: 2019 },
      { season: 4, episodes: 9, year: 2022 }
    ],
    languages: ["en"],
    subtitles: ["en", "es", "fr", "de"]
  }
]);