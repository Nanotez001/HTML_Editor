html_head = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
@media (max-width: 600px) {
  table.spec-table,
  table.spec-table thead,
  table.spec-table tbody,
  table.spec-table th,
  table.spec-table td,
  table.spec-table tr {
    display: block;
    width: 100%;
    box-sizing: border-box;
  }
  table.spec-table,  
  table.spec-table tr {
    margin-bottom: 10px;
    border-radius: 8px;
    padding: 1px;
    background: none;
    word-wrap: break-word;  
    overflow-wrap: break-word; 
    white-space: normal;     
  }

  table.spec-table th,
  table.spec-table td {
    padding: 7px 0;
    border: none;
    border-radius: 5px;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
    text-indent: 5px;
  }
}

body {
    font-family: 'Sarabun','Kanit', 'Noto Sans Thai',sans-serif;
    margin: 20px;
    background-color: #f9f9f9;
    color: #333;
}
.container {
    max-width: 900px;
    margin: auto;
    background: #fff;
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 0 12px rgba(0,0,0,0.1);
}
h1 {
    font-size: 1.8rem;
    color: #111;
}
h2 {
    font-size: 1.4rem;
    margin-top: 30px;
    border-bottom: 2px solid #ddd;
    padding-bottom: 5px;
}
h3 {
    font-size: 1.5rem;
}
ul {
    list-style: disc;
    padding-left: 20px;
}
table.spec-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}
th, td {
    padding: 7px 0;
    border: none;
    border-radius: 5px;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
    text-indent: 5px;
}
th {
    background-color: #f0f0f0;
}

</style>
</head>
<body>
<div class="container">
"""

html_footer = """
</div>
</body>
</html>
"""















