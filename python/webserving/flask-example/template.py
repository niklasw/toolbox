

# Lägg märke till {{keyword}} nedan. Dessa är parametrar
# i Jinja2.Temlate

template='''
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Bildkarusellen</title>
  <meta name="description" content="Bildkarusellen">
  <meta name="author" content="SitePoint">

  <link rel="stylesheet" href="css/styles.css?v=1.0">

</head>

<form action="/backward/" method="post">
    <button name="previousButton" type="submit">Left</button>
</form>

<img src="{{prevImage}}" width="200" alt="Image2"/>
<img src="{{image}}" width="800" alt="Image2"/>
<img src="{{nextImage}}" width="200" alt="Image2"/>

<form action="/forward/" method="post">
    <button name="previousButton" type="submit">Right</button>
</form>

</html>
'''
