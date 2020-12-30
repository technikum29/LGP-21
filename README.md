# LPG-21 Programs
Programs for the LPG-21 vintage computer (read from paper tape)

## Einleseroutine für Papertapes

**Hardware:**
- Ghielmetti Lochstreifenleser Typ FER 201
- Adapterplatine von Jürgen Müller direckt auf den Schnittstellen-Anschluss gesteckt

**Software:**
- [lgp21read.py](lpg21read.py): Python-Programm zum Lesen vom Lochstreifenleser und Abspeichern der Files
- [lgp21convert.py](lpg21convert.py): Python-Programm zum nachträglichen konvertieren von raw-Files (s.u.)

## Bedienung

1. Reader über USB anschließen
2. Nachsehen, unter welchem COM-Port er angemeldet wurde (Windows Geräte-Manager)
3. Python-Programm "lgp21read.py" starten
4. Nummer des (Pseudo-) COM-Ports eingeben, an dem der Reader hängt
5. Lochstreifen einlegen, Klappe schließen
6. Ziel-Dateinamen eingeben. 
7. Lochstreifen wird eingelesen und Dateien geschrieben   
8. Klappe öffnen, mit neuem Lochstreifen weiter unter 5.

Die Reihenfolge der Schritte 5 und 6 kann man auch tauschen, z.B. um den einzugebenden Dateinamen vom Lochstreifen
abzulesen. Die Reader-Steuerung merkt, wenn man die Klappe am Reader schließt, wartet dann noch 1.5 Sekunden, damit
man die Finger wegbekommt, und fängt dann zu lesen an. (Wenn sie nicht auf den PC und die Eingabe eines Dateinamens warten muss.)

## Datenformat:

Es werden immer drei Dateien geschrieben -- vgl. die Kommentare zu Beginn des Python-Programms:
* `.raw`: raw 8-bit binary data, including leading/trailing $00 bytes
* `.flx`: 6-bit Flexowriter code, $00 bytes removed
* `.asc`: converted to ASCII, $00 bytes removed

Comments:

*  Raw bit order on the tape is 76543/210, where 0 denotes the LSB.
*  Flexowriter bit order on the paper tape is ..612/345,
   where '.' denotes unused holes, '/' the transport holes, 6 the LSB.
*  The .flx file has bits in the order 123456.

Die Wandlung in .flx und .asc entfernt, wie oben angegeben, die $00-Bytes aus dem Datenstrom (ungestanzte Positionen,
insbesondere zu Beginn und am Ende des Streifens). Mir sind dann allerdings Zweifel gekommen, ob das wirklich wünschenswert
ist, weil manchmal auch mitten in den Streifen solche Null-Sequenzen vorkommen. Das separate Programm "lgp21convert.py"
nimmt sich die .raw-Dateien vor (in denen die Nullen noch drin sind) und wandelt sie unter Erhaltung der Nullen in .flx2
und .asc2 Files. Was besser ist, kann ich noch nicht sagen. Wenn Du erstmal nur mit lgp21read.py alles einliest, kann mans
später die .raw Dateien immer noch wandeln.

## Übersicht der Programme

Siehe [Uebersicht LPG21_Papertapes](Uebersicht LPG21_Papertapes.md).

## Siehe auch

* http://www.e-basteln.de/computing/lgp21/lgp21-replica/ (especially *replica project files*)
* https://technikum29.de/de/rechnertechnik/fruehe-computer.php#lgp21
