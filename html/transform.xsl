<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei">


  <xsl:output method="html" indent="yes" encoding="UTF-8"/>


  <xsl:template match="/">
    <section class="tei-item">
      <!-- 每个 item 的标题 -->
      <h2>
        <xsl:value-of select="//tei:teiHeader//tei:title[1]"/>
      </h2>


      <div class="meta">
        <xsl:if test="//tei:author">
          <p><strong>Author:</strong>
            <xsl:value-of select="//tei:author[1]"/>
          </p>
        </xsl:if>

        <xsl:if test="//tei:publisher">
          <p><strong>Publisher:</strong>
            <xsl:value-of select="//tei:publisher[1]"/>
          </p>
        </xsl:if>

        <xsl:if test="//tei:date">
          <p><strong>Date:</strong>
            <xsl:value-of select="//tei:date[1]/@when | //tei:date[1]"/>
          </p>
        </xsl:if>
      </div>

      <div class="content">
        <xsl:apply-templates select="//tei:text"/>
      </div>
    </section>
  </xsl:template>



  <xsl:template match="tei:text">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="tei:body">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="tei:div">
    <div class="tei-div">
      <xsl:if test="tei:head">
        <h3><xsl:value-of select="tei:head[1]"/></h3>
      </xsl:if>
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>

  <xsl:template match="tei:lb">
    <br/>
  </xsl:template>

  <xsl:template match="tei:pb">
    <hr/>
    <p><em>Page <xsl:value-of select="@n"/></em></p>
  </xsl:template>

  <xsl:template match="tei:figure">
    <div class="figure">
      <xsl:if test="tei:head">
        <h3><xsl:value-of select="tei:head"/></h3>
      </xsl:if>
      <xsl:if test="tei:graphic">
        <img>
          <xsl:attribute name="src">
            <xsl:value-of select="tei:graphic/@url"/>
          </xsl:attribute>
        </img>
      </xsl:if>
      <xsl:if test="tei:figDesc">
        <p><xsl:value-of select="tei:figDesc"/></p>
      </xsl:if>
    </div>
  </xsl:template>

  <xsl:template match="tei:listPlace">
    <div class="places">
      <h3>Places</h3>
      <ul>
        <xsl:for-each select="tei:place">
          <li>
            <strong><xsl:value-of select="tei:placeName"/></strong>
            <xsl:text> — </xsl:text>
            <xsl:value-of select="tei:desc"/>
          </li>
        </xsl:for-each>
      </ul>
    </div>
  </xsl:template>

  <xsl:template match="tei:*">
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
