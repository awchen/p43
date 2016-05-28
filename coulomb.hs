import System.IO
import System.Environment

k = 8.987e9

--force :: Double -> Double -> Double -> Double
--force q1 q2 dist = (k * q1 * q2) / (distance^2)

distance :: (Double, Double) -> (Double, Double) -> Double
distance a b = sqrt((snd b - snd a)^2 + (fst b - fst a)^2)

-- returns a difference vector (x, y) with direction a -> b
diffVec :: (Double, Double) -> (Double, Double) -> (Double, Double)
diffVec a b = (fst b - fst a, snd b - snd a)

-- returns a unit vector (x, y) with direction a -> b
unitVec :: (Double, Double) -> (Double, Double) -> (Double, Double)
unitVec a b = mapTuple f (diffVec a b)
    where f c = c / (distance a b)

mapTuple :: (a -> b) -> (a, a) -> (b, b)
mapTuple f (a1, a2) = (f a1, f a2)

main :: IO ()
main = do
    args <- getArgs
    if length args < 1
        then putStrLn "First argument should be the path to the input file."
        else putStrLn $ args !! 0