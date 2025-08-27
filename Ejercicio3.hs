-- Calculadora de división - Haskell

dividir :: Double -> Double -> Either String Double
dividir _ 0 = Left "Error: división por cero."
dividir x y = Right (x / y)

-- Versión que devuelve String (útil para mostrar directamente)
dividirStr :: Double -> Double -> String
dividirStr x y = case dividir x y of
  Left err -> err
  Right r  -> "Resultado: " ++ show r

-- Ejemplo de uso en main
main :: IO ()
main = do
  putStrLn "Ingresa el numerador:"
  nStr <- getLine
  putStrLn "Ingresa el divisor:"
  dStr <- getLine
  case (reads nStr :: [(Double,String)], reads dStr :: [(Double,String)]) of
    ([(n,"")], [(d,"")]) -> putStrLn (dividirStr n d)
    _ -> putStrLn "Entrada inválida: por favor ingresa números válidos."
