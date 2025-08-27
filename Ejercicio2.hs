-- Verificación de contraseña - Haskell
import Data.Char (toLower)

-- Función que compara dos Strings ignorando mayúsculas/minúsculas
coincidenIgnoreCase :: String -> String -> Bool
coincidenIgnoreCase a b = map toLower (trim a) == map toLower (trim b)
  where
    -- trim simple para eliminar espacios al inicio/fin
    trim = f . f
      where f = reverse . dropWhile (== ' ')

-- Ejemplo de uso en main (opcional)
main :: IO ()
main = do
  putStrLn "Ingresa la contraseña almacenada:"
  almacenada <- getLine
  putStrLn "Ingresa la contraseña de prueba:"
  entrada <- getLine
  if coincidenIgnoreCase almacenada entrada
    then putStrLn "Contraseñas coinciden."
    else putStrLn "Contraseñas NO coinciden."
