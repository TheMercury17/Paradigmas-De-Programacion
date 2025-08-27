-- Verificador de edad legal - Haskell

-- Función pura que devuelve un String
mayorDeEdad :: Int -> String
mayorDeEdad edad
  | edad < 0  = "Edad inválida: no puede ser negativa."
  | edad >= 18 = "Eres mayor de edad."
  | otherwise  = "Eres menor de edad."

-- Ejemplo de main para uso por consola (opcional)
main :: IO ()
main = do
  putStrLn "Ingresa tu edad:"
  linea <- getLine
  case reads linea :: [(Int, String)] of
    [(edad, "")] -> putStrLn (mayorDeEdad edad)
    _            -> putStrLn "Entrada inválida: por favor ingresa un número entero."
