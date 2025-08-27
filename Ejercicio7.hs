-- Evaluación de los empleados - Haskell

evaluarEmpleado :: Double -> (String, Double)
evaluarEmpleado p
  | p < 0 || p > 100 = error "La puntuacion debe estar entre 0 y 100."
  | p >= 90          = ("Excelente", 1000.0)
  | p >= 75          = ("Muy bueno", 500.0)
  | p >= 60          = ("Aceptable", 200.0)
  | otherwise        = ("Necesita mejorar", 0.0)

-- Helper para mostrar el resultado sin romper en tiempo de ejecución
mostrarEvaluacion :: Double -> String
mostrarEvaluacion p
  | p < 0 || p > 100 = "Entrada inválida: la puntuación debe estar entre 0 y 100."
  | otherwise =
      let (nivel, recompensa) = evaluarEmpleado p
      in "Nivel de rendimiento: " ++ nivel ++ "\nRecompensa monetaria: $" ++ show recompensa

-- Ejemplo de main para consola
main :: IO ()
main = do
  putStrLn "Ingresa la puntuación del empleado (0-100):"
  linea <- getLine
  case reads linea :: [(Double, String)] of
    [(p, "")] -> putStrLn (mostrarEvaluacion p)
    _         -> putStrLn "Entrada inválida: por favor ingresa un número entre 0 y 100."