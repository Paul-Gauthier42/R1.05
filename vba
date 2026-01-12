Option Explicit

Sub ImporterCsvEtGraphPortScan()
    Dim cheminFichier As Variant
    Dim wsData As Worksheet
    Dim wb As Workbook
   
    Set wb = ThisWorkbook
   
    ' Demander le fichier CSV
    cheminFichier = Application.GetOpenFilename( _
                    FileFilter:="Fichiers CSV (*.csv),*.csv", _
                    Title:="Sélectionner le fichier d'analyse CSV")
   
    If cheminFichier = False Then
        MsgBox "Aucun fichier sélectionné.", vbInformation
        Exit Sub
    End If
   
    ' Créer / vider la feuille DATA_CSV
    On Error Resume Next
    Set wsData = wb.Worksheets("DATA_CSV")
    On Error GoTo 0
   
    If wsData Is Nothing Then
        Set wsData = wb.Worksheets.Add
        wsData.Name = "DATA_CSV"
    Else
        wsData.Cells.Clear
    End If
   
    ' Import du CSV dans DATA_CSV
    With wsData.QueryTables.Add(Connection:="TEXT;" & cheminFichier, Destination:=wsData.Range("A1"))
        .TextFileParseType = xlDelimited
        .TextFileCommaDelimiter = True
        .TextFileSemicolonDelimiter = True
        .TextFileOtherDelimiter = False
        .TextFileColumnDataTypes = Array(1)
        .AdjustColumnWidth = True
        .Refresh BackgroundQuery:=False
        .Delete
    End With
   
    ' Création du graphique
    CreerGraphPortScan_VBA wb, wsData
    MsgBox "Graphique port scan généré.", vbInformation
End Sub


Sub CreerGraphPortScan_VBA(wb As Workbook, wsData As Worksheet)
    Dim ws As Worksheet
    Dim colSrc As Long, colPort As Long
    Dim lastRow As Long, i As Long
    Dim dict As Object            ' src_ip -> autre dictionnaire (ports)
    Dim dictPorts As Object
    Dim ip As Variant, port As String
    Dim ligneOut As Long
    Dim ch As ChartObject
   
    ' Adapter ici si les noms d'en-tête sont différents
    colSrc = TrouverColonne(wsData, "src_ip")
    colPort = TrouverColonne(wsData, "dst_port")
    If colSrc = 0 Or colPort = 0 Then
        MsgBox "Colonnes 'src_ip' ou 'dst_port' introuvables dans DATA_CSV." & vbCrLf & _
               "Vérifie exactement le nom des en-têtes.", vbExclamation
        Exit Sub
    End If
   
    On Error Resume Next
    Set ws = wb.Worksheets("PortScan_Sources")
    On Error GoTo 0
   
    If ws Is Nothing Then
        Set ws = wb.Worksheets.Add
        ws.Name = "PortScan_Sources"
    Else
        ws.Cells.Clear
    End If
   
    ' Lecture des données dans des dictionnaires
    lastRow = wsData.Cells(wsData.Rows.Count, colSrc).End(xlUp).Row
    Set dict = CreateObject("Scripting.Dictionary")
   
    For i = 2 To lastRow
        ip = wsData.Cells(i, colSrc).Value
        port = CStr(wsData.Cells(i, colPort).Value)
       
        If ip <> "" And port <> "" Then
            If Not dict.exists(ip) Then
                Set dictPorts = CreateObject("Scripting.Dictionary")
                dict.Add ip, dictPorts
            Else
                Set dictPorts = dict(ip)
            End If
            If Not dictPorts.exists(port) Then
                dictPorts.Add port, True
            End If
        End If
    Next i
   
    ' Écriture des résultats (IP / nb ports distincts)
    ws.Range("A1").Value = "src_ip"
    ws.Range("B1").Value = "nb_ports_distincts"
   
    ligneOut = 2
    For Each ip In dict.keys
        Set dictPorts = dict(ip)
        ws.Cells(ligneOut, 1).Value = ip
        ws.Cells(ligneOut, 2).Value = dictPorts.Count
        ligneOut = ligneOut + 1
    Next ip
   
    If ligneOut = 2 Then
        MsgBox "Aucune donnée valide pour le port scan.", vbInformation
        Exit Sub
    End If
   
    lastRow = ligneOut - 1
   
    ' Tri décroissant sur nb_ports_distincts, top 10
    ws.Range("A1:B" & lastRow).Sort Key1:=ws.Range("B2"), Order1:=xlDescending, Header:=xlYes
    If lastRow > 11 Then
        ws.Range("A12:B" & lastRow).ClearContents
        lastRow = 11
    End If
   
    ' Création du graphique
    Set ch = ws.ChartObjects.Add(Left:=300, Top:=20, Width:=500, Height:=300)
   
    With ch.Chart
        .ChartType = xlColumnClustered
        .SetSourceData Source:=ws.Range("A1:B" & lastRow)
        .HasTitle = True
        .ChartTitle.Text = "Sources possibles de port scan (ports distincts par src_ip)"
        .Axes(xlCategory).HasTitle = True
        .Axes(xlCategory).AxisTitle.Text = "IP source"
        .Axes(xlValue).HasTitle = True
        .Axes(xlValue).AxisTitle.Text = "Nombre de ports distincts"
    End With
End Sub


Function TrouverColonne(ws As Worksheet, nomColonne As String) As Long
    Dim c As Range
    For Each c In ws.Rows(1).Cells
        If LCase$(Trim$(c.Value)) = LCase$(nomColonne) Then
            TrouverColonne = c.Column
            Exit Function
        End If
    Next c
    TrouverColonne = 0
End Function