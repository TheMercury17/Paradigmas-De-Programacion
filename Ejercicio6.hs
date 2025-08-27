-- Asignación grupal - Haskell
import Data.Char (toUpper, isAlpha)
import Data.List (stripPrefix)

-- Devuelve String con el grupo o mensaje de error
asignarGrupo :: String -> String -> String
asignarGrupo nombre genero
  | null nombreTrim = "Entrada inválida: el nombre no puede estar vacío."
  | not (isAlpha primera) = "Entrada inválida: el nombre debe comenzar con una letra."
  | generoNorm == 'M' =
      if primera <= 'M' then nombreTrim ++ ": Grupo A (Deportes)"
      else nombreTrim ++ ": Grupo B (Ciencias)"
  | generoNorm == 'F' =
      if primera <= 'M' then nombreTrim ++ ": Grupo C (Arte)"
      else nombreTrim ++ ": Grupo D (Matemáticas)"
  | otherwise = "Debe ingresar un género válido"
  where
    nombreTrim = dropWhile (== ' ') $ reverse $ dropWhile (== ' ') $ reverse nombre
    primera = toUpper (head nombreTrim)
    generoNorm = case (map toUpper (dropWhile (== ' ') genero)) of
                   (g:_) -> g
                   []    -> 'O'  -- tratado como otro

-- Ejemplo de main para consola
main :: IO ()
main = do
  putStrLn "Ingresa tu nombre:"
  n <- getLine
  putStrLn "Ingresa tu género (M/F):"
  g <- getLine
  putStrLn (asignarGrupo n g)