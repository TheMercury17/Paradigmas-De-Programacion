--               TALLER DE HASKELL: Funcion sucesora
--                  Andres Sebastián Coral Vallejo
--                       ._________________.
--                      |.---------------.|
--                      ||    A.S.C.V.   ||
--                      ||   -._ .-.     ||
--                      ||   -._| | |    ||
--                      ||   -._|"|"|    ||
--                      ||    MERCURY    ||
--                      ||_______________||
--                      /.-.-.-.-.-.-.-.-.\
--                     /.-.-.-.-.-.-.-.-.-.\
--                    /.-.-.-.-.-.-.-.-.-.-.\
--                   /______/__________\___o_\
--                   \_______________________/

import Text.Read (readMaybe)
import System.IO (hFlush, stdout)
import System.Info (os)
import Data.List (isPrefixOf)
import System.Process (callCommand)
import Data.Char (toLower)

-- Parte 1: funciones básicas
sucesor :: Int -> Int
sucesor n = n + 1

predecesor :: Int -> Int
predecesor n = n - 1

-- Suma usando sucesor: add a b aplica sucesor b veces a a
add :: Int -> Int -> Int
add a b
  | b <= 0    = a
  | otherwise = add (sucesor a) (b - 1)

-- Multiplicación como suma repetida
multiplicar :: Int -> Int -> Int
multiplicar _ b | b <= 0 = 0
multiplicar a b = add a (multiplicar a (b - 1))

-- Parte 2: resta y división usando predecesor y restas repetidas
restar :: Int -> Int -> Int
restar a b
  | b <= 0    = a
  | otherwise = restar (predecesor a) (b - 1)

dividir :: Int -> Int -> Int
dividir _ 0 = error "Error: division por cero (divisor = 0)"
dividir a b
  | a < b     = 0
  | otherwise = 1 + dividir (restar a b) b

-- Parte 3: números reales (suma directa)
addReal :: Double -> Double -> Double
addReal x y = x + y

-- Detectar sistema operativo (Windows o Linux/Mac)
esWindows :: Bool
esWindows = any (`isPrefixOf` os) ["mingw", "cygwin", "win"]

-- Limpiar pantalla
limpiarPantalla :: IO ()
limpiarPantalla =
  if esWindows
    then callCommand "cls"
    else callCommand "clear"

-- leer y validar entradas
leerIntNoNeg :: String -> IO Int
leerIntNoNeg prompt = do
  putStr prompt
  hFlush stdout
  line <- getLine
  case readMaybe line :: Maybe Int of
    Just n | n >= 0 -> return n
    _ -> putStrLn "Entrada invalida. Debes ingresar un entero >= 0. Intenta de nuevo." >> leerIntNoNeg prompt

leerIntPos :: String -> IO Int
leerIntPos prompt = do
  putStr prompt
  hFlush stdout
  line <- getLine
  case readMaybe line :: Maybe Int of
    Just n | n > 0 -> return n
    _ -> putStrLn "Entrada invalida. Debes ingresar un entero > 0. Intenta de nuevo." >> leerIntPos prompt

leerDouble :: String -> IO Double
leerDouble prompt = do
  putStr prompt
  hFlush stdout
  line <- getLine
  case readMaybe line :: Maybe Double of
    Just d -> return d
    _ -> putStrLn "Entrada invalida. Ingresa un numero real (ej: 3.14). Intenta de nuevo." >> leerDouble prompt

-- Después de mostrar un resultado, dar opción de salir o volver al menú
postResultado :: IO ()
postResultado = do
  putStr "Escribe 'salir' para salir o presiona Enter para volver al menu: "
  hFlush stdout
  resp <- getLine
  if map toLower resp == "salir"
    then putStrLn "Saliendo..."
    else do
      limpiarPantalla
      menu

-- Menú
menu :: IO ()
menu = do
  putStrLn "=== Calculadora con sucesor/predecesor ==="
  putStrLn "Elige la operación:"
  putStrLn " 1) Sumar (enteros >= 0) [usando sucesor]"
  putStrLn " 2) Multiplicar (enteros >= 0) [repeticion de suma]"
  putStrLn " 3) Restar (enteros >= 0) [usando predecesor]"
  putStrLn " 4) Dividir (enteros >= 0) [restas repetidas -- divisor > 0]"
  putStrLn " 5) Sumar reales (Float/Double)"
  putStrLn " 6) Salir"
  putStr "Opcion: "
  hFlush stdout
  opt <- getLine
  case opt of
    "1" -> do
      limpiarPantalla
      a <- leerIntNoNeg "Digite el dato a : "
      b <- leerIntNoNeg "Digite el dato b : "
      putStrLn $ "Resultado: " ++ show (add a b)
      putStrLn ""
      postResultado
    "2" -> do
      limpiarPantalla
      a <- leerIntNoNeg "Digite el dato a : "
      b <- leerIntNoNeg "Digite el dato b : "
      putStrLn $ "Resultado: " ++ show (multiplicar a b)
      putStrLn ""
      postResultado
    "3" -> do
      limpiarPantalla
      a <- leerIntNoNeg "Digite el dato a : "
      b <- leerIntNoNeg "Digite el dato b : "
      putStrLn $ "Resultado: " ++ show (restar a b)
      putStrLn ""
      postResultado
    "4" -> do
      limpiarPantalla
      a <- leerIntNoNeg "Digite el dato a : "
      b <- leerIntPos "Digite el dato b : "
      putStrLn $ "Resultado: " ++ show (dividir a b)
      putStrLn ""
      postResultado
    "5" -> do
      limpiarPantalla
      x <- leerDouble "Digite el dato x : "
      y <- leerDouble "Digite el dato y : "
      putStrLn $ "Resultado (addReal): " ++ show (addReal x y)
      putStrLn ""
      postResultado
    "6" -> putStrLn "Saliendo..."
    _   -> putStrLn "Opcion no válida." >> putStrLn "" >> menu

main :: IO ()
main = menu

