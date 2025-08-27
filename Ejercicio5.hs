-- Comprobador de elegibilidad de impuestos - Haskell
-- Criterios por defecto: edad mínima 18, ingreso mensual mínimo 2000.0

import Text.Read (readMaybe)

edadMinima :: Int
edadMinima = 18

umbralIngreso :: Double
umbralIngreso = 2000.0

-- Función que devuelve Bool: True = debe pagar impuestos
necesitaPagarImpuestos :: Int -> Double -> Bool
necesitaPagarImpuestos edad ingreso
  | edad < 0 || ingreso < 0 = error "Edad e ingreso deben ser no negativos."
  | otherwise = edad >= edadMinima && ingreso >= umbralIngreso

-- Versión que devuelve String lista para mostrar
mostrarObligacion :: Int -> Double -> String
mostrarObligacion edad ingreso
  | edad < 0 || ingreso < 0 = "Entrada inválida: edad o ingreso negativo."
  | necesitaPagarImpuestos edad ingreso = "Según los criterios, debes pagar impuestos."
  | otherwise = "Según los criterios, NO debes pagar impuestos."

-- Ejemplo de main para consola
main :: IO ()
main = do
  putStrLn "Ingresa tu edad:"
  edadStr <- getLine
  putStrLn "Ingresa tu ingreso mensual:"
  ingresoStr <- getLine
  case (readMaybe edadStr :: Maybe Int, readMaybe ingresoStr :: Maybe Double) of
    (Just e, Just i) -> putStrLn (mostrarObligacion e i)
    _                -> putStrLn "Entrada inválida: por favor ingresa números válidos."
