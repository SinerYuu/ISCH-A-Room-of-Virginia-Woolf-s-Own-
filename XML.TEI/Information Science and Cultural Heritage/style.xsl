<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <!-- 根模板 -->
  <xsl:template match="/">
    <html>
      <head>
        <title>TEI 文本显示</title>
        <style>
          body { font-family: serif; line-height: 1.6; padding: 2em; white-space: pre-wrap; }
        </style>
      </head>
      <body>
        <xsl:apply-templates select="//tei:text"/>
      </body>
    </html>
  </xsl:template>

  <!-- 段落 -->
  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>

  <!-- 换行 -->
  <xsl:template match="tei:lb">
    <br/>
  </xsl:template>

  <!-- 换页标记忽略（也可自定义） -->
  <xsl:template match="tei:pb">
    <hr style="border: none; border-top: 1px dashed gray; margin: 1em 0"/>
  </xsl:template>

  <!-- 默认模板：显示文字 -->
  <xsl:template match="text()">
    <xsl:value-of select="."/>
  </xsl:template>

</xsl:stylesheet>
