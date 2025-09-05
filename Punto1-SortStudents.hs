-- Ordenación declarativa (Haskell)
-- Se ordena una lista de (Nombre, Nota) por:
--  1) Nota descendente
--  2) Si las notas empatan, por Nombre ascendente
--
-- Este archivo contiene una lista de ejemplo (mismos 12 estudiantes que el .py)
-- y una función pura `sortStudents` que describe QUÉ se quiere hacer (no CÓMO).

module Main where

import Data.List (sortBy)

type Name = String
type Score = Int
type Student = (Name, Score)

-- En esto se usa sortBy con una comparación compuesta.
-- Primero compara s2 s1 -> fuerza orden descendente por nota
-- En caso de igualdad (EQ) -> compara n1 n2 (nombre ascendente)

sortStudents :: [Student] -> [Student]
sortStudents = sortBy cmp
  where
    cmp :: Student -> Student -> Ordering
    cmp (n1,s1) (n2,s2) =
      case compare s2 s1 of   -- comparar s2 vs s1 para obtener descendente
        EQ -> compare n1 n2   -- si hay empate, ordenar por nombre (ascendente)
        ord -> ord

-- Lista de ejemplo (12 estudiantes).
example :: [Student]
example =
  [ ("Maria",     92)
  , ("Valentina", 92)
  , ("Juan",      85)
  , ("Carlos",    85)
  , ("Sofia",     78)
  , ("Diego",     74)
  , ("Andres",    68)
  , ("Daniela",   68)
  , ("Mateo",     55)
  , ("Lucia",     55)
  , ("Catalina",  40)
  , ("Luis",      30)
  ]

main :: IO ()
main = do
  putStrLn "Lista original de estudiantes (nombre, nota):"
  mapM_ print example

  putStrLn "\nLista ordenada (nota descendente, nombre ascendente en empates):"
  mapM_ print (sortStudents example)

-- NOTA:
-- Haskell trabaja con datos inmutables por defecto; sortStudents devuelve
-- una nueva lista ordenada. No hay efectos laterales en la función pura.

