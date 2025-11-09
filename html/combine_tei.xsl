<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                exclude-result-prefixes="tei"
                version="1.0">

<xsl:output method="html" encoding="UTF-8" indent="yes"/>

<!-- 根模板：遍历 main.xml -->
<xsl:template match="/">
<html>
<head>
    <meta charset="UTF-8"/>
    <title>Virginia Woolf Digital Collection</title>
    <style>
        body { font-family: Georgia, serif; margin: 2em; background: #fafafa; color: #222; }
        h1 { border-bottom: 2px solid #ccc; padding-bottom: 0.2em; }
        h2 { color: #5a3e85; margin-top: 1.5em; }
        h3 { margin-top: 1em; color: #333; }
        .error { color: red; font-style: italic; }
    </style>
</head>
<body>
    <h1>Virginia Woolf Digital Collection</h1>

    <!-- 遍历各 section -->
    <xsl:for-each select="collection/section">
        <h2><xsl:value-of select="@title"/></h2>

        <!-- 遍历文件 -->
        <xsl:for-each select="file">
            <h3><xsl:value-of select="@label"/></h3>
            <xsl:variable name="path" select="@href"/>

            <!-- 尝试加载外部 XML -->
            <xsl:variable name="doc" select="document($path)"/>

            <xsl:choose>
                <!-- 如果有正文 -->
                <xsl:when test="$doc//tei:text//tei:body">
                    <xsl:apply-templates select="$doc//tei:teiHeader" mode="meta"/>
                    <xsl:apply-templates select="$doc//tei:text//tei:body"/>
                </xsl:when>

                <!-- 如果只有图片 -->
                <xsl:when test="$doc//tei:graphic">
                    <xsl:for-each select="$doc//tei:graphic">
                        <p><img src="{@url}" alt="{@n}" style="max-width:400px"/></p>
                    </xsl:for-each>
                </xsl:when>

                <!-- 否则提示无内容 -->
                <xsl:otherwise>
                    <p class="error">⚠️ 无法加载：<xsl:value-of select="$path"/></p>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:for-each>
</body>
</html>
</xsl:template>

<!-- 提取元数据 -->
<xsl:template match="tei:teiHeader" mode="meta">
    <p><b>Title:</b> <xsl:value-of select=".//tei:titleStmt/tei:title"/></p>
    <p><b>Author:</b> <xsl:value-of select=".//tei:titleStmt/tei:author"/></p>
    <xsl:if test=".//tei:availability/p">
        <p><xsl:value-of select=".//tei:availability/p"/></p>
    </xsl:if>
    <xsl:if test=".//tei:projectDesc/p">
        <p><xsl:value-of select=".//tei:projectDesc/p"/></p>
    </xsl:if>
</xsl:template>

<!-- 正文处理 -->
<xsl:template match="tei:body">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="tei:div|tei:p|tei:head|tei:lb|tei:pb">
    <xsl:choose>
        <xsl:when test="self::tei:head"><h4><xsl:value-of select="."/></h4></xsl:when>
        <xsl:when test="self::tei:p"><p><xsl:apply-templates/></p></xsl:when>
        <xsl:when test="self::tei:lb"><br/></xsl:when>
        <xsl:when test="self::tei:pb"><hr/></xsl:when>
        <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>
