-- ============================================================
-- Tourism Experience Analytics
-- SQL Analysis Queries
-- ============================================================


-- Query 1: Top 10 Most Visited Attractions
SELECT
    Attraction,
    COUNT(*) AS VisitCount
FROM tourism_data
GROUP BY Attraction
ORDER BY VisitCount DESC
LIMIT 10;


-- Query 2: Average Rating by Attraction
SELECT
    Attraction,
    ROUND(AVG(Rating), 2) AS AverageRating,
    COUNT(*) AS RatingCount
FROM tourism_data
GROUP BY Attraction
ORDER BY AverageRating DESC;


-- Query 3: VisitMode Distribution
SELECT
    VisitMode,
    COUNT(*) AS VisitorCount
FROM tourism_data
GROUP BY VisitMode
ORDER BY VisitorCount DESC;


-- Query 4: Average Rating by VisitMode
SELECT
    VisitMode,
    ROUND(AVG(Rating), 2) AS AverageRating,
    COUNT(*) AS VisitorCount
FROM tourism_data
GROUP BY VisitMode
ORDER BY AverageRating DESC;


-- Query 5: Most Popular Attraction Types
SELECT
    AttractionType,
    COUNT(*) AS VisitCount
FROM tourism_data
GROUP BY AttractionType
ORDER BY VisitCount DESC
LIMIT 10;

-- Query 1: Top 10 Most Visited Attractions
SELECT
    Attraction,
    COUNT(*) AS VisitCount
FROM tourism_data
GROUP BY Attraction
ORDER BY VisitCount DESC
LIMIT 10;