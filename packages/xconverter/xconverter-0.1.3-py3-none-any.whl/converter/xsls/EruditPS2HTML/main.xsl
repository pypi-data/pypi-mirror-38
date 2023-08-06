<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    xmlns:str="http://exslt.org/strings" xmlns:converter="converter"
    exclude-result-prefixes="converter xs str" version="2.0">

    <xsl:import href="utils.xsl"/>
    <xsl:param name="assets_path"/>
    <xsl:variable name="document_language" select="article/@xml:lang"/>
    
    <xsl:template match="article">
        <xsl:variable name="lang" select="@xml:lang"/>
        <html>
            <head>
                <title><xsl:value-of select="front/journal-meta/journal-title-group/journal-title"/>: <xsl:value-of select="front/article-meta/title-group/article-title"/></title>
                <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
            </head>
            <body> 
                <div class="cover">              
                    <div class="journal-meta">
                        <xsl:apply-templates select="front/journal-meta/journal-title-group/journal-title"/>
                        <xsl:apply-templates select="front/journal-meta/journal-title-group/journal-subtitle"/>
                    </div>
                    <div class="issue-meta">
                        <xsl:apply-templates select="front/article-meta/issue-title"/>
                        <div class="issue-number">
                            <dl>
                                <xsl:apply-templates select="front/article-meta/volume"/>
                                <xsl:apply-templates select="front/article-meta/issue"/>
                                <xsl:apply-templates select="front/article-meta/pub-date[@date-type='issue']/season"/>
                                <xsl:apply-templates select="front/article-meta/pub-date[@date-type='issue']/year"/>
                            </dl>
                        </div>
                    </div>
                    <div class="article-meta">
                        <xsl:apply-templates select="front/article-meta/title-group/article-title"/>
                        <xsl:apply-templates select="front/article-meta/title-group/subtitle"/>
                    </div>
                    <div class="license">
                        <xsl:value-of select="front/article-meta/permissions/license/license-p"/>
                    </div> 
                </div>
                <div class="article">
                    <div class="front">
                        <div class="title-group">
                            <xsl:apply-templates select="front/article-meta/title-group/article-title"/>
                            <xsl:apply-templates select="front/article-meta/title-group/subtitle"/>
                        </div>
                        <xsl:apply-templates select="front/article-meta/article-id[@pub-id-type = 'doi']" />
                        <xsl:apply-templates select="front/article-meta/contrib-group"/>
                        <div class="abstract-group">
                            <xsl:apply-templates select="front/article-meta/abstract"/>
                            <xsl:apply-templates select="front/article-meta/trans-abstract"/>
                        </div>
                    </div>
                    <div class="body_back">
                        <xsl:apply-templates select="body"/>
                        <div class="back">
                            <xsl:if test="count(back//ack) > 0">
                                <div class="ack-group">
                                    <div class="title">
                                        <xsl:call-template name="translation">
                                            <xsl:with-param name="key">Acknowledgement</xsl:with-param>
                                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                                        </xsl:call-template>
                                    </div>
                                    <xsl:apply-templates select="back//ack"/>
                                </div>
                            </xsl:if>
                            <xsl:apply-templates select="back/fn-group"/>
                            <xsl:apply-templates select="back/ref-list"/>
                            <xsl:if test="count(back//notes[@notes-type='annex']) > 0">
                                <div class="annexes">
                                    <div class="title">
                                        <xsl:call-template name="translation">
                                            <xsl:with-param name="key">Annexes</xsl:with-param>
                                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                                        </xsl:call-template>
                                    </div>
                                    <xsl:apply-templates select="back/notes[@notes-type='annex']"/>
                                </div>
                            </xsl:if>
                            <xsl:if test="count(//bio) > 0">
                                <div class="bio-notes">
                                    <div class="title">
                                        <xsl:call-template name="translation">
                                            <xsl:with-param name="key">Biographic Notes</xsl:with-param>
                                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                                        </xsl:call-template>
                                    </div>
                                    <xsl:apply-templates select="//bio"/>
                                </div>
                            </xsl:if>
                        </div>
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="body">
        <div class="body">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="license-p">
        <xsl:apply-templates select="." mode="text_with_formating"/>
    </xsl:template>

    <xsl:template match="issue-title">
        <div class="issue-title">
           <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>

    <xsl:template match="issue">
        <dt class="label-number">
           <xsl:call-template name="translation">
               <xsl:with-param name="key">issue</xsl:with-param>
               <xsl:with-param name="language"><xsl:value-of select="$document_language"/></xsl:with-param>
           </xsl:call-template>
        </dt>
        <dd class="content-number"><xsl:value-of select="."/></dd>
    </xsl:template>
    
    <xsl:template match="volume">
        <dt class="label-volume">
            <xsl:call-template name="translation">
                <xsl:with-param name="key">volume</xsl:with-param>
                <xsl:with-param name="language"><xsl:value-of select="$document_language"/></xsl:with-param>
            </xsl:call-template>
        </dt>
        <dd class="content-volume"><xsl:value-of select="."/></dd>
    </xsl:template>
    
    <xsl:template match="season">
        <dt class="label-season">
            <xsl:call-template name="translation">
                <xsl:with-param name="key">season</xsl:with-param>
                <xsl:with-param name="language"><xsl:value-of select="$document_language"/></xsl:with-param>
            </xsl:call-template>
        </dt>
        <dd class="content-season"><xsl:value-of select="."/></dd>
    </xsl:template>

    <xsl:template match="year">
        <dt class="label-year">
            <xsl:call-template name="translation">
                <xsl:with-param name="key">year</xsl:with-param>
                <xsl:with-param name="language"><xsl:value-of select="$document_language"/></xsl:with-param>
            </xsl:call-template>
        </dt>
        <dd class="content-year"><xsl:value-of select="."/></dd>
    </xsl:template>

    <xsl:template match="journal-title">
        <div class="journal-title">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>
    
    <xsl:template match="journal-subtitle">
        <div class="journal-subtitle">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>
    
    <xsl:template match="notes">
        <div class="annex">
            <xsl:apply-templates select="*"/>
        </div>        
    </xsl:template>
    
    <xsl:template match="bio">
        <div class="bio">
            <xsl:apply-templates select="."  mode="text_with_formating" />
        </div>        
    </xsl:template>

    <xsl:template match="ack">
        <div class="ack">
            <xsl:apply-templates select="."  mode="text_with_formating" />
        </div>        
    </xsl:template>
    
    <xsl:template match="article-title">
        <div class="article-title">
            <xsl:apply-templates select="."  mode="text_with_formating" />
        </div>
    </xsl:template>
    
    <xsl:template match="subtitle">
        <div class="subtitle">
            <xsl:apply-templates select="." mode="text_with_formating" />
        </div>
    </xsl:template>
    
    <xsl:template match="sec">
        <div class="sec">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote">
        <div class="disp-quote">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type= 'dedicatory']">
        <div class="dedicatory">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type= 'example']">
        <div class="example">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type= 'block-citation']">
        <div class="block-citation">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type= 'verbatim']">
        <div class="verbatim">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type= 'epigraph']">
        <div class="epigraph">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="attrib">
        <div class="attrib">
            <xsl:apply-templates select="." mode="text_with_formating" />
        </div>
    </xsl:template>
    
    <xsl:template match="sec/label"/>
 
    <xsl:template match="fn-group">
        <xsl:variable name="lang" select="@xml:lang"/>
        <div class="footnotes">
            <xsl:choose>
                <xsl:when test="title != ''">
                    <xsl:apply-templates select="title"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="title">
                        <xsl:call-template name="translation">
                            <xsl:with-param name="key">Footnotes</xsl:with-param>
                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                        </xsl:call-template>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="fn"/>
        </div>
    </xsl:template>

    <xsl:template match="ref-list">
        <xsl:variable name="lang" select="@xml:lang"/>
        <div class="ref-list">
            <xsl:choose>
                <xsl:when test="title != ''">
                    <xsl:apply-templates select="title"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="title">
                        <xsl:call-template name="translation">
                            <xsl:with-param name="key">References</xsl:with-param>
                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                        </xsl:call-template>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="ref"/>
        </div>
    </xsl:template>

    <xsl:template match="fn">
        <div class="footnote">
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:apply-templates select="label" mode="footnote"/>
            <xsl:apply-templates select="p"/>
        </div>
    </xsl:template>
    
    <xsl:template match="label" mode="footnote">
        <div class="label">
            [<a><xsl:attribute name="href">#rel<xsl:value-of select="../@id"/></xsl:attribute><xsl:value-of select="."/></a>]
        </div>
    </xsl:template>

    <xsl:template match="label">
        <div class="label">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>
    
    <xsl:template match="caption">
        <div class="caption">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>
    
    <xsl:template match="xref">
        <sup>
            <a href="#">
                <xsl:attribute name="href">#<xsl:value-of select="@rid"/></xsl:attribute>
                <xsl:attribute name="id">rel<xsl:value-of select="@rid"/></xsl:attribute>
                <xsl:attribute name="class">xref</xsl:attribute>
                <xsl:value-of select="."/>
            </a>
        </sup>
    </xsl:template>
 
    <xsl:template match="ref">
        <xsl:apply-templates select="element-citation/styled-content"/>
    </xsl:template>
    
    <xsl:template match="styled-content">
        <div class="ref">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>

    <xsl:template match="abstract|trans-abstract">
        <xsl:variable name="lang" select="@xml:lang"/>
        <div class="abstract">
            <xsl:choose>
                <xsl:when test="title != ''">
                    <xsl:apply-templates select="title"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="title">
                         <xsl:call-template name="translation">
                             <xsl:with-param name="key">Abstract</xsl:with-param>
                             <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                         </xsl:call-template>
                    </div>
                </xsl:otherwise>
            </xsl:choose>  
            <xsl:apply-templates select="p"/>
            <xsl:apply-templates select="../kwd-group[@xml:lang = $lang]"/>
        </div>
    </xsl:template>
    
    <xsl:template match="kwd-group">
        <xsl:variable name="lang" select="@xml:lang"/>
        <div class="kwd-group">
            <xsl:choose>
                <xsl:when test="title != ''">
                    <xsl:apply-templates select="title"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="title">
                        <xsl:call-template name="translation">
                            <xsl:with-param name="key">Keywords</xsl:with-param>
                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                        </xsl:call-template>
                    </div>
                </xsl:otherwise>
            </xsl:choose>  
            <ul>
                <xsl:apply-templates select="kwd"/>
            </ul>
        </div>
    </xsl:template>
    
    <xsl:template match="kwd">
        <li>
            <xsl:value-of select="."/>;
        </li>
    </xsl:template>
    
    <xsl:template match="title">
        <div class="title">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>

    <xsl:template match="p">
        <p>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </p>
    </xsl:template>

    <xsl:template match="contrib-group">
        <div class="contrib-group">
            <xsl:apply-templates select="contrib"/>
        </div>        
    </xsl:template>
    
    <xsl:template match="contrib">
        <div class="contrib">
            <div class="name">
                <xsl:value-of select="name/given-names"/>&#160;<xsl:value-of select="name/surname"/>
            </div> 
            <xsl:apply-templates select="string-name"/>
            <xsl:apply-templates select="xref" mode="affiliation"/>
            <xsl:apply-templates select="email"/>
        </div>
    </xsl:template>

    <xsl:template match="string-name[@content-type='alias']">
        <div class="alias">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>
    
    <xsl:template match="email">
        <div class="email">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <xsl:template match="xref" mode="affiliation">
        <xsl:variable name="aff_id"><xsl:value-of select="@rid"/></xsl:variable>
        <xsl:apply-templates select="//aff[@id=$aff_id]/institution"/>
    </xsl:template>

    <xsl:template match="institution">
        <div class="institution">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <xsl:template match="article-id">
        <div class="article-id">http://dxdoi.crossref.org/<xsl:value-of select="."/></div>        
    </xsl:template>
    
    <xsl:template match="boxed-text">
        <div class="boxed-text">
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="boxed-header">
                        <xsl:apply-templates select="label|caption"/>   
                    </div>
                    <div class="boxed-content">
                        <xsl:apply-templates select="sec|p|disp-quote"/>  
                    </div>
                    <xsl:apply-templates select="attrib"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="boxed-content">
                        <xsl:apply-templates select="*"/>  
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>

    <xsl:template match="caption">
        <div class="caption">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>

    <xsl:template match="list[@list-type = 'bullet']">
        <ul>
            <xsl:apply-templates select="*"/>
        </ul>
    </xsl:template>

    <xsl:template match="list[@list-type = 'order']">
        <ol>
            <xsl:apply-templates select="*"/>
        </ol>
    </xsl:template>

    <xsl:template match="list-item">
        <li><xsl:apply-templates select="." mode="text_with_formating" /></li>
    </xsl:template>

    <xsl:template match="italic">
        <i><xsl:apply-templates select="." mode="text_with_formating" /></i>
    </xsl:template>
    
    <xsl:template match="bold">
        <b><xsl:apply-templates select="." mode="text_with_formating" /></b>
    </xsl:template>
    
    <xsl:template match="sc">
        <small>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </small>
    </xsl:template>
    
    <xsl:template match="overline">
        <overline>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </overline>
    </xsl:template>
    
    <xsl:template match="underline">
        <underline>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </underline>
    </xsl:template>
    
    <xsl:template match="sup">
        <sup>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </sup>
    </xsl:template>
    
    <xsl:template match="sub">
        <sub>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </sub>
    </xsl:template>
    
    <xsl:template match="def-list">
        <dl>
            <xsl:apply-templates select="def-item"/>
        </dl>
    </xsl:template>
    
    <xsl:template match="def-item">
        <dt><xsl:apply-templates select="term" mode="text_with_formating"/></dt>
        <dd><xsl:apply-templates select="def" mode="text_with_formating"/></dd>
    </xsl:template>
    
    <xsl:template match="disp-formula-group">
        <div class="disp-formula-group">
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="disp-formula-group-header">
                        <xsl:apply-templates select="label|caption"/>   
                    </div>
                    <div class="disp-formula-group-content">
                        <xsl:apply-templates select="disp-formula|disp-formula-group"/>  
                    </div>
                </xsl:when>
                <xsl:otherwise>
                    <div class="disp-formula-group-content">
                        <xsl:apply-templates select="*"/>  
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>
    
    <xsl:template match="disp-formula">
        <div class="disp-formula">
            <xsl:apply-templates select="*|text()"/>
        </div>
    </xsl:template>

    <xsl:template match="fig-group">
        <div class="fig-group">
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="fig-group-header">
                        <xsl:apply-templates select="label|caption"/>   
                    </div>
                    <div class="fig-group-content">
                        <xsl:apply-templates select="fig|graphic|media"/>  
                    </div>
                </xsl:when>
                <xsl:otherwise>
                    <div class="fig-group-content">
                        <xsl:apply-templates select="*"/>  
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>        
    </xsl:template>

    <xsl:template match="fig">
        <div class="fig">
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="fig-header">
                        <xsl:apply-templates select="label|caption"/>   
                    </div>
                    <div class="fig-content">
                        <xsl:apply-templates select="graphic|media"/>  
                    </div>
                    <xsl:apply-templates select="attrib"/>
                    <xsl:apply-templates select="permissions"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="fig-content">
                        <xsl:apply-templates select="*"/>  
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>
    
    <xsl:template match="ext-link">
        <xsl:choose>
            <xsl:when test="(. != '') and (. != @xlink:href)">
                <xsl:value-of select="."/> (<a><xsl:attribute name="href"><xsl:value-of select="@xlink:href"/></xsl:attribute><xsl:value-of select="@xlink:href"/></a>)
            </xsl:when>
            <xsl:otherwise>
                (<a><xsl:attribute name="href"><xsl:value-of select="@xlink:href"/></xsl:attribute><xsl:value-of select="@xlink:href"/></a>)
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="inline-graphic">
        <div class="inline-graphic">
            <img>
                <xsl:attribute name="src"><xsl:if test="$assets_path != ''"><xsl:value-of select="$assets_path"/>/</xsl:if><xsl:value-of select="@xlink:href"/></xsl:attribute>
            </img>
        </div>
    </xsl:template>
    
    <xsl:template match="inline-formula">
        <xsl:apply-templates select="." mode="text_with_formating"/>
    </xsl:template>

    <xsl:template match="graphic">
        <div>
            <xsl:attribute name="class">image-<xsl:value-of select="@position"/></xsl:attribute>
            <img>
                <xsl:attribute name="src"><xsl:if test="$assets_path != ''"><xsl:value-of select="$assets_path"/>/</xsl:if><xsl:value-of select="@xlink:href"/></xsl:attribute>
            </img>
        </div>
    </xsl:template>
    
    <xsl:template match="media[@mimetype='video']">
        <div class="media-video">
            <video>
                <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
                <xsl:attribute name="controls">controls</xsl:attribute>
                <source>
                    <xsl:attribute name="src"><xsl:if test="$assets_path != ''"><xsl:value-of select="$assets_path"/>/</xsl:if><xsl:value-of select="@xlink:href"/></xsl:attribute>
                </source>
            </video>
        </div>
    </xsl:template>
    
    <xsl:template match="table-wrap-group">
        <div class="table-wrap-group">
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="table-wrap-group-header">
                        <xsl:apply-templates select="label|caption"/>   
                    </div>
                    <div class="table-wrap-group-content">
                        <xsl:apply-templates select="table-wrap"/>  
                    </div>
                </xsl:when>
                <xsl:otherwise>
                    <div class="table-wrap-group-content">
                        <xsl:apply-templates select="*"/>  
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>        
    </xsl:template>
    
    <xsl:template match="table-wrap">
        <div class="table-wrap">
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="table-wrap-header">
                        <xsl:apply-templates select="label|caption"/>   
                    </div>
                    <div class="table-wrap-content">
                        <xsl:apply-templates select="media|graphic|table"/>  
                    </div>
                    <xsl:apply-templates select="attrib"/>
                    <xsl:apply-templates select="permissions"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="table-wrap-content">
                        <xsl:apply-templates select="*"/>  
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>
    
    <xsl:template match="table">
        <xsl:copy-of select="."/>
    </xsl:template>

    <xsl:template match="mml:math">
        <math xmlns="http://www.w3.org/1998/Math/MathML">
            <xsl:copy-of select="@*"/>
            <xsl:apply-templates mode="mathml"/>
        </math>
    </xsl:template>

    <xsl:template match="*" mode="mathml">
        <xsl:element name="{local-name()}" xmlns="http://www.w3.org/1998/Math/MathML">
            <xsl:copy-of select="@*"/>
            <xsl:apply-templates mode="mathml"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="* | text()" mode="text_with_formating">
        <xsl:apply-templates select="* | text()"/>
    </xsl:template>

    <xsl:template match="* | @*">
        <PENDING-TREATMENT>
            <xsl:copy-of select="."/>
        </PENDING-TREATMENT>
    </xsl:template>
 
</xsl:stylesheet>