```mermaid

sequenceDiagram
  participant main
  participant laitehallinto
  participant rautatietori
  participant ratikka6
  participant bussi244
  participant kioski
  participant kallen_kortti
  
    main ->> laitehallinto: HKLLaitehallinto()
    laitehallinto ->> rautatietori: Lataajalaite()
    laitehallinto ->> ratikka6: Lukijalaite()
    laitehallinto ->> bussi244 = Lukijalaite()

```
