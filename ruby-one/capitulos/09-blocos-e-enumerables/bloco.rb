def para_cada_turno
  yield "6h"
  yield "13h"
end

para_cada_turno { |hora| puts "carga das #{hora}" }
