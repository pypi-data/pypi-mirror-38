@REM ----------------------------------------------------------------------------
@REM  Copyright 2001-2006 The Apache Software Foundation.
@REM
@REM  Licensed under the Apache License, Version 2.0 (the "License");
@REM  you may not use this file except in compliance with the License.
@REM  You may obtain a copy of the License at
@REM
@REM       http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM  Unless required by applicable law or agreed to in writing, software
@REM  distributed under the License is distributed on an "AS IS" BASIS,
@REM  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM  See the License for the specific language governing permissions and
@REM  limitations under the License.
@REM ----------------------------------------------------------------------------
@REM
@REM   Copyright (c) 2001-2006 The Apache Software Foundation.  All rights
@REM   reserved.

@echo off

set ERROR_CODE=0

:init
@REM Decide how to startup depending on the version of windows

@REM -- Win98ME
if NOT "%OS%"=="Windows_NT" goto Win9xArg

@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" @setlocal

@REM -- 4NT shell
if "%eval[2+2]" == "4" goto 4NTArgs

@REM -- Regular WinNT shell
set CMD_LINE_ARGS=%*
goto WinNTGetScriptDir

@REM The 4NT Shell from jp software
:4NTArgs
set CMD_LINE_ARGS=%$
goto WinNTGetScriptDir

:Win9xArg
@REM Slurp the command line arguments.  This loop allows for an unlimited number
@REM of arguments (up to the command line limit, anyway).
set CMD_LINE_ARGS=
:Win9xApp
if %1a==a goto Win9xGetScriptDir
set CMD_LINE_ARGS=%CMD_LINE_ARGS% %1
shift
goto Win9xApp

:Win9xGetScriptDir
set SAVEDIR=%CD%
%0\
cd %0\..\.. 
set BASEDIR=%CD%
cd %SAVEDIR%
set SAVE_DIR=
goto repoSetup

:WinNTGetScriptDir
set BASEDIR=%~dp0\..

:repoSetup
set REPO=


if "%JAVACMD%"=="" set JAVACMD=java

if "%REPO%"=="" set REPO=%BASEDIR%\repo

set CLASSPATH="%BASEDIR%"\etc;"%REPO%"\io\jenkins\jenkinsfile-runner-bootstrap\1.0-SNAPSHOT\jenkinsfile-runner-bootstrap-1.0-SNAPSHOT.jar;"%REPO%"\args4j\args4j\2.33\args4j-2.33.jar;"%REPO%"\commons-io\commons-io\2.5\commons-io-2.5.jar;"%REPO%"\io\jenkins\jenkinsfile-runner-setup\1.0-SNAPSHOT\jenkinsfile-runner-setup-1.0-SNAPSHOT.jar;"%REPO%"\org\jenkins-ci\main\jenkins-test-harness\2.38\jenkins-test-harness-2.38.jar;"%REPO%"\org\eclipse\jetty\jetty-webapp\9.4.5.v20170502\jetty-webapp-9.4.5.v20170502.jar;"%REPO%"\org\eclipse\jetty\jetty-xml\9.4.5.v20170502\jetty-xml-9.4.5.v20170502.jar;"%REPO%"\org\eclipse\jetty\jetty-util\9.4.5.v20170502\jetty-util-9.4.5.v20170502.jar;"%REPO%"\org\eclipse\jetty\jetty-servlet\9.4.5.v20170502\jetty-servlet-9.4.5.v20170502.jar;"%REPO%"\org\eclipse\jetty\jetty-security\9.4.5.v20170502\jetty-security-9.4.5.v20170502.jar;"%REPO%"\org\eclipse\jetty\jetty-server\9.4.5.v20170502\jetty-server-9.4.5.v20170502.jar;"%REPO%"\javax\servlet\javax.servlet-api\3.1.0\javax.servlet-api-3.1.0.jar;"%REPO%"\org\eclipse\jetty\jetty-http\9.4.5.v20170502\jetty-http-9.4.5.v20170502.jar;"%REPO%"\org\eclipse\jetty\jetty-io\9.4.5.v20170502\jetty-io-9.4.5.v20170502.jar;"%REPO%"\junit\junit\4.12\junit-4.12.jar;"%REPO%"\org\hamcrest\hamcrest-core\1.3\hamcrest-core-1.3.jar;"%REPO%"\org\hamcrest\hamcrest-library\1.3\hamcrest-library-1.3.jar;"%REPO%"\org\jenkins-ci\main\jenkins-test-harness-htmlunit\2.18-1\jenkins-test-harness-htmlunit-2.18-1.jar;"%REPO%"\xalan\xalan\2.7.2\xalan-2.7.2.jar;"%REPO%"\xalan\serializer\2.7.2\serializer-2.7.2.jar;"%REPO%"\org\apache\commons\commons-lang3\3.4\commons-lang3-3.4.jar;"%REPO%"\xerces\xercesImpl\2.11.0\xercesImpl-2.11.0.jar;"%REPO%"\xml-apis\xml-apis\1.4.01\xml-apis-1.4.01.jar;"%REPO%"\net\sourceforge\nekohtml\nekohtml\1.9.22\nekohtml-1.9.22.jar;"%REPO%"\net\sourceforge\cssparser\cssparser\0.9.16\cssparser-0.9.16.jar;"%REPO%"\org\w3c\css\sac\1.3\sac-1.3.jar;"%REPO%"\commons-logging\commons-logging\1.2\commons-logging-1.2.jar;"%REPO%"\org\eclipse\jetty\websocket\websocket-client\9.2.12.v20150709\websocket-client-9.2.12.v20150709.jar;"%REPO%"\org\eclipse\jetty\websocket\websocket-common\9.2.12.v20150709\websocket-common-9.2.12.v20150709.jar;"%REPO%"\org\eclipse\jetty\websocket\websocket-api\9.2.12.v20150709\websocket-api-9.2.12.v20150709.jar;"%REPO%"\org\jvnet\hudson\embedded-rhino-debugger\1.2\embedded-rhino-debugger-1.2.jar;"%REPO%"\org\netbeans\modules\org-netbeans-insane\RELEASE72\org-netbeans-insane-RELEASE72.jar;"%REPO%"\com\github\stephenc\findbugs\findbugs-annotations\1.3.9-1\findbugs-annotations-1.3.9-1.jar;"%REPO%"\org\jenkins-ci\main\jenkins-war\2.89\jenkins-war-2.89.war;"%REPO%"\org\jenkins-ci\main\jenkins-core\2.89\jenkins-core-2.89.jar;"%REPO%"\org\jenkins-ci\plugins\icon-shim\icon-set\1.0.5\icon-set-1.0.5.jar;"%REPO%"\org\jenkins-ci\main\cli\2.89\cli-2.89.jar;"%REPO%"\org\jenkins-ci\version-number\1.4\version-number-1.4.jar;"%REPO%"\org\jenkins-ci\crypto-util\1.1\crypto-util-1.1.jar;"%REPO%"\org\jvnet\hudson\jtidy\4aug2000r7-dev-hudson-1\jtidy-4aug2000r7-dev-hudson-1.jar;"%REPO%"\com\google\inject\guice\4.0\guice-4.0.jar;"%REPO%"\javax\inject\javax.inject\1\javax.inject-1.jar;"%REPO%"\aopalliance\aopalliance\1.0\aopalliance-1.0.jar;"%REPO%"\org\jruby\ext\posix\jna-posix\1.0.3-jenkins-1\jna-posix-1.0.3-jenkins-1.jar;"%REPO%"\com\github\jnr\jnr-posix\3.0.41\jnr-posix-3.0.41.jar;"%REPO%"\com\github\jnr\jnr-ffi\2.1.4\jnr-ffi-2.1.4.jar;"%REPO%"\com\github\jnr\jffi\1.2.15\jffi-1.2.15.jar;"%REPO%"\com\github\jnr\jffi\1.2.15\jffi-1.2.15-native.jar;"%REPO%"\org\ow2\asm\asm\5.0.3\asm-5.0.3.jar;"%REPO%"\org\ow2\asm\asm-commons\5.0.3\asm-commons-5.0.3.jar;"%REPO%"\org\ow2\asm\asm-analysis\5.0.3\asm-analysis-5.0.3.jar;"%REPO%"\org\ow2\asm\asm-tree\5.0.3\asm-tree-5.0.3.jar;"%REPO%"\org\ow2\asm\asm-util\5.0.3\asm-util-5.0.3.jar;"%REPO%"\com\github\jnr\jnr-x86asm\1.0.2\jnr-x86asm-1.0.2.jar;"%REPO%"\com\github\jnr\jnr-constants\0.9.8\jnr-constants-0.9.8.jar;"%REPO%"\org\kohsuke\trilead-putty-extension\1.2\trilead-putty-extension-1.2.jar;"%REPO%"\org\jenkins-ci\trilead-ssh2\build-217-jenkins-11\trilead-ssh2-build-217-jenkins-11.jar;"%REPO%"\net\i2p\crypto\eddsa\0.2.0\eddsa-0.2.0.jar;"%REPO%"\org\connectbot\jbcrypt\jbcrypt\1.0.0\jbcrypt-1.0.0.jar;"%REPO%"\org\kohsuke\stapler\stapler-groovy\1.253\stapler-groovy-1.253.jar;"%REPO%"\org\kohsuke\stapler\stapler-jelly\1.253\stapler-jelly-1.253.jar;"%REPO%"\org\jenkins-ci\commons-jelly\1.1-jenkins-20120928\commons-jelly-1.1-jenkins-20120928.jar;"%REPO%"\org\jenkins-ci\dom4j\dom4j\1.6.1-jenkins-4\dom4j-1.6.1-jenkins-4.jar;"%REPO%"\org\kohsuke\stapler\stapler-jrebel\1.253\stapler-jrebel-1.253.jar;"%REPO%"\org\kohsuke\stapler\stapler\1.253\stapler-1.253.jar;"%REPO%"\javax\annotation\javax.annotation-api\1.2\javax.annotation-api-1.2.jar;"%REPO%"\commons-discovery\commons-discovery\0.4\commons-discovery-0.4.jar;"%REPO%"\org\jvnet\tiger-types\2.2\tiger-types-2.2.jar;"%REPO%"\com\google\code\findbugs\jsr305\2.0.1\jsr305-2.0.1.jar;"%REPO%"\org\kohsuke\windows-package-checker\1.2\windows-package-checker-1.2.jar;"%REPO%"\org\kohsuke\stapler\stapler-adjunct-zeroclipboard\1.3.5-1\stapler-adjunct-zeroclipboard-1.3.5-1.jar;"%REPO%"\org\kohsuke\stapler\stapler-adjunct-timeline\1.5\stapler-adjunct-timeline-1.5.jar;"%REPO%"\org\kohsuke\stapler\stapler-adjunct-codemirror\1.3\stapler-adjunct-codemirror-1.3.jar;"%REPO%"\com\infradna\tool\bridge-method-annotation\1.13\bridge-method-annotation-1.13.jar;"%REPO%"\org\kohsuke\stapler\json-lib\2.4-jenkins-2\json-lib-2.4-jenkins-2.jar;"%REPO%"\net\sf\ezmorph\ezmorph\1.0.6\ezmorph-1.0.6.jar;"%REPO%"\commons-httpclient\commons-httpclient\3.1-jenkins-1\commons-httpclient-3.1-jenkins-1.jar;"%REPO%"\org\jenkins-ci\bytecode-compatibility-transformer\1.8\bytecode-compatibility-transformer-1.8.jar;"%REPO%"\org\kohsuke\asm5\5.0.1\asm5-5.0.1.jar;"%REPO%"\org\jenkins-ci\task-reactor\1.4\task-reactor-1.4.jar;"%REPO%"\org\jvnet\localizer\localizer\1.24\localizer-1.24.jar;"%REPO%"\antlr\antlr\2.7.6\antlr-2.7.6.jar;"%REPO%"\org\jvnet\hudson\xstream\1.4.7-jenkins-1\xstream-1.4.7-jenkins-1.jar;"%REPO%"\jfree\jfreechart\1.0.9\jfreechart-1.0.9.jar;"%REPO%"\jfree\jcommon\1.0.12\jcommon-1.0.12.jar;"%REPO%"\org\apache\ant\ant\1.8.4\ant-1.8.4.jar;"%REPO%"\org\apache\ant\ant-launcher\1.8.4\ant-launcher-1.8.4.jar;"%REPO%"\commons-lang\commons-lang\2.6\commons-lang-2.6.jar;"%REPO%"\commons-digester\commons-digester\2.1\commons-digester-2.1.jar;"%REPO%"\commons-beanutils\commons-beanutils\1.8.3\commons-beanutils-1.8.3.jar;"%REPO%"\org\apache\commons\commons-compress\1.10\commons-compress-1.10.jar;"%REPO%"\javax\mail\mail\1.4.4\mail-1.4.4.jar;"%REPO%"\org\jvnet\hudson\activation\1.1.1-hudson-1\activation-1.1.1-hudson-1.jar;"%REPO%"\jaxen\jaxen\1.1-beta-11\jaxen-1.1-beta-11.jar;"%REPO%"\commons-jelly\commons-jelly-tags-fmt\1.0\commons-jelly-tags-fmt-1.0.jar;"%REPO%"\commons-jelly\commons-jelly-tags-xml\1.1\commons-jelly-tags-xml-1.1.jar;"%REPO%"\org\jvnet\hudson\commons-jelly-tags-define\1.0.1-hudson-20071021\commons-jelly-tags-define-1.0.1-hudson-20071021.jar;"%REPO%"\org\jenkins-ci\commons-jexl\1.1-jenkins-20111212\commons-jexl-1.1-jenkins-20111212.jar;"%REPO%"\org\acegisecurity\acegi-security\1.0.7\acegi-security-1.0.7.jar;"%REPO%"\org\springframework\spring-jdbc\1.2.9\spring-jdbc-1.2.9.jar;"%REPO%"\org\springframework\spring-dao\1.2.9\spring-dao-1.2.9.jar;"%REPO%"\oro\oro\2.0.8\oro-2.0.8.jar;"%REPO%"\log4j\log4j\1.2.9\log4j-1.2.9.jar;"%REPO%"\org\codehaus\groovy\groovy-all\2.4.11\groovy-all-2.4.11.jar;"%REPO%"\jline\jline\2.12\jline-2.12.jar;"%REPO%"\org\fusesource\jansi\jansi\1.11\jansi-1.11.jar;"%REPO%"\org\springframework\spring-webmvc\2.5.6.SEC03\spring-webmvc-2.5.6.SEC03.jar;"%REPO%"\org\springframework\spring-beans\2.5.6.SEC03\spring-beans-2.5.6.SEC03.jar;"%REPO%"\org\springframework\spring-context\2.5.6.SEC03\spring-context-2.5.6.SEC03.jar;"%REPO%"\org\springframework\spring-context-support\2.5.6.SEC03\spring-context-support-2.5.6.SEC03.jar;"%REPO%"\org\springframework\spring-web\2.5.6.SEC03\spring-web-2.5.6.SEC03.jar;"%REPO%"\org\springframework\spring-core\2.5.6.SEC03\spring-core-2.5.6.SEC03.jar;"%REPO%"\org\springframework\spring-aop\2.5.6.SEC03\spring-aop-2.5.6.SEC03.jar;"%REPO%"\xpp3\xpp3\1.1.4c\xpp3-1.1.4c.jar;"%REPO%"\javax\servlet\jsp\jstl\javax.servlet.jsp.jstl-api\1.2.1\javax.servlet.jsp.jstl-api-1.2.1.jar;"%REPO%"\org\slf4j\jcl-over-slf4j\1.7.25\jcl-over-slf4j-1.7.25.jar;"%REPO%"\org\slf4j\log4j-over-slf4j\1.7.25\log4j-over-slf4j-1.7.25.jar;"%REPO%"\com\sun\xml\txw2\txw2\20110809\txw2-20110809.jar;"%REPO%"\javax\xml\stream\stax-api\1.0-2\stax-api-1.0-2.jar;"%REPO%"\relaxngDatatype\relaxngDatatype\20020414\relaxngDatatype-20020414.jar;"%REPO%"\org\jvnet\winp\winp\1.25\winp-1.25.jar;"%REPO%"\org\jenkins-ci\memory-monitor\1.9\memory-monitor-1.9.jar;"%REPO%"\org\codehaus\woodstox\wstx-asl\3.2.9\wstx-asl-3.2.9.jar;"%REPO%"\stax\stax-api\1.0.1\stax-api-1.0.1.jar;"%REPO%"\org\jenkins-ci\jmdns\3.4.0-jenkins-3\jmdns-3.4.0-jenkins-3.jar;"%REPO%"\net\java\dev\jna\jna\4.2.1\jna-4.2.1.jar;"%REPO%"\org\kohsuke\akuma\1.10\akuma-1.10.jar;"%REPO%"\org\kohsuke\libpam4j\1.8\libpam4j-1.8.jar;"%REPO%"\org\kohsuke\libzfs\0.8\libzfs-0.8.jar;"%REPO%"\com\sun\solaris\embedded_su4j\1.1\embedded_su4j-1.1.jar;"%REPO%"\net\java\sezpoz\sezpoz\1.12\sezpoz-1.12.jar;"%REPO%"\org\kohsuke\jinterop\j-interop\2.0.6-kohsuke-1\j-interop-2.0.6-kohsuke-1.jar;"%REPO%"\org\kohsuke\jinterop\j-interopdeps\2.0.6-kohsuke-1\j-interopdeps-2.0.6-kohsuke-1.jar;"%REPO%"\org\samba\jcifs\jcifs\1.2.19\jcifs-1.2.19.jar;"%REPO%"\org\jvnet\robust-http-client\robust-http-client\1.2\robust-http-client-1.2.jar;"%REPO%"\commons-codec\commons-codec\1.9\commons-codec-1.9.jar;"%REPO%"\org\kohsuke\access-modifier-annotation\1.11\access-modifier-annotation-1.11.jar;"%REPO%"\commons-fileupload\commons-fileupload\1.3.1-jenkins-2\commons-fileupload-1.3.1-jenkins-2.jar;"%REPO%"\com\google\guava\guava\11.0.1\guava-11.0.1.jar;"%REPO%"\com\jcraft\jzlib\1.1.3-kohsuke-1\jzlib-1.1.3-kohsuke-1.jar;"%REPO%"\org\jenkins-ci\main\remoting\3.13\remoting-3.13.jar;"%REPO%"\org\jenkins-ci\constant-pool-scanner\1.2\constant-pool-scanner-1.2.jar;"%REPO%"\org\jenkins-ci\modules\instance-identity\2.1\instance-identity-2.1.jar;"%REPO%"\io\github\stephenc\crypto\self-signed-cert-generator\1.0.0\self-signed-cert-generator-1.0.0.jar;"%REPO%"\org\jenkins-ci\modules\ssh-cli-auth\1.4\ssh-cli-auth-1.4.jar;"%REPO%"\org\jenkins-ci\modules\slave-installer\1.6\slave-installer-1.6.jar;"%REPO%"\org\jenkins-ci\modules\windows-slave-installer\1.9.1\windows-slave-installer-1.9.1.jar;"%REPO%"\org\jenkins-ci\modules\launchd-slave-installer\1.2\launchd-slave-installer-1.2.jar;"%REPO%"\org\jenkins-ci\modules\upstart-slave-installer\1.1\upstart-slave-installer-1.1.jar;"%REPO%"\org\jenkins-ci\modules\systemd-slave-installer\1.1\systemd-slave-installer-1.1.jar;"%REPO%"\org\jenkins-ci\ui\jquery-detached\1.2.1\jquery-detached-1.2.1-core-assets.jar;"%REPO%"\org\jenkins-ci\ui\bootstrap\1.3.2\bootstrap-1.3.2-core-assets.jar;"%REPO%"\org\jenkins-ci\ui\jquery-detached\1.2\jquery-detached-1.2.jar;"%REPO%"\org\jenkins-ci\ui\handlebars\1.1.1\handlebars-1.1.1-core-assets.jar;"%REPO%"\io\jenkins\jenkinsfile-runner-payload\1.0-SNAPSHOT\jenkinsfile-runner-payload-1.0-SNAPSHOT.jar;"%REPO%"\io\jenkins\jenkinsfile-runner-payload-dependencies\1.0-SNAPSHOT\jenkinsfile-runner-payload-dependencies-1.0-SNAPSHOT.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-cps\2.41\workflow-cps-2.41.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-step-api\2.13\workflow-step-api-2.13.jar;"%REPO%"\org\jenkins-ci\plugins\scm-api\2.0.8\scm-api-2.0.8.jar;"%REPO%"\org\jenkins-ci\plugins\structs\1.7\structs-1.7.jar;"%REPO%"\com\cloudbees\groovy-cps\1.20\groovy-cps-1.20.jar;"%REPO%"\org\jenkins-ci\ui\ace-editor\1.0.1\ace-editor-1.0.1.jar;"%REPO%"\com\cloudbees\diff4j\1.2\diff4j-1.2.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-api\2.26\workflow-api-2.26.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-job\2.17\workflow-job-2.17.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-multibranch\2.9.2\workflow-multibranch-2.9.2.jar;"%REPO%"\org\jenkins-ci\plugins\branch-api\1.11\branch-api-1.11.jar;"%REPO%"\org\jenkins-ci\plugins\cloudbees-folder\5.12\cloudbees-folder-5.12.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-scm-step\2.6\workflow-scm-step-2.6.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-scm-step\2.4\workflow-scm-step-2.4-tests.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-basic-steps\2.3\workflow-basic-steps-2.3.jar;"%REPO%"\org\jenkins-ci\plugins\mailer\1.13\mailer-1.13.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-durable-task-step\2.9\workflow-durable-task-step-2.9.jar;"%REPO%"\org\jenkins-ci\plugins\durable-task\1.13\durable-task-1.13.jar;"%REPO%"\org\jenkins-ci\plugins\workflow\workflow-support\2.17\workflow-support-2.17.jar;"%REPO%"\org\jboss\marshalling\jboss-marshalling-river\1.4.12.jenkins-3\jboss-marshalling-river-1.4.12.jenkins-3.jar;"%REPO%"\org\jboss\marshalling\jboss-marshalling\1.4.12.jenkins-3\jboss-marshalling-1.4.12.jenkins-3.jar;"%REPO%"\org\jenkins-ci\plugins\script-security\1.39\script-security-1.39.jar;"%REPO%"\org\kohsuke\groovy-sandbox\1.16\groovy-sandbox-1.16.jar;"%REPO%"\org\slf4j\slf4j-jdk14\1.7.25\slf4j-jdk14-1.7.25.jar;"%REPO%"\org\slf4j\slf4j-api\1.7.25\slf4j-api-1.7.25.jar;"%REPO%"\commons-collections\commons-collections\3.2.2\commons-collections-3.2.2.jar;"%REPO%"\org\jenkins-ci\symbol-annotation\1.7\symbol-annotation-1.7.jar;"%REPO%"\org\jenkins-ci\annotation-indexer\1.12\annotation-indexer-1.12.jar;"%REPO%"\io\jenkins\jenkinsfile-runner\1.0-SNAPSHOT\jenkinsfile-runner-1.0-SNAPSHOT.jar

set ENDORSED_DIR=
if NOT "%ENDORSED_DIR%" == "" set CLASSPATH="%BASEDIR%"\%ENDORSED_DIR%\*;%CLASSPATH%

if NOT "%CLASSPATH_PREFIX%" == "" set CLASSPATH=%CLASSPATH_PREFIX%;%CLASSPATH%

@REM Reaching here means variables are defined and arguments have been captured
:endInit

%JAVACMD% %JAVA_OPTS%  -classpath %CLASSPATH% -Dapp.name="jenkinsfile-runner" -Dapp.repo="%REPO%" -Dapp.home="%BASEDIR%" -Dbasedir="%BASEDIR%" io.jenkins.jenkinsfile.runner.bootstrap.Bootstrap %CMD_LINE_ARGS%
if %ERRORLEVEL% NEQ 0 goto error
goto end

:error
if "%OS%"=="Windows_NT" @endlocal
set ERROR_CODE=%ERRORLEVEL%

:end
@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" goto endNT

@REM For old DOS remove the set variables from ENV - we assume they were not set
@REM before we started - at least we don't leave any baggage around
set CMD_LINE_ARGS=
goto postExec

:endNT
@REM If error code is set to 1 then the endlocal was done already in :error.
if %ERROR_CODE% EQU 0 @endlocal


:postExec

if "%FORCE_EXIT_ON_ERROR%" == "on" (
  if %ERROR_CODE% NEQ 0 exit %ERROR_CODE%
)

exit /B %ERROR_CODE%
