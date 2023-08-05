#!/bin/bash

IimBriefDescription="NOTYET: Short Description Of The Module"

ORIGIN="
* Revision And Libre-Halaal CopyLeft -- Part Of ByStar -- Best Used With Blee
"

####+BEGIN: bx:dblock:bash:top-of-file :vc "cvs" partof: "bystar" :copyleft "halaal+brief"
typeset RcsId="$Id: roPerf-bearerTokenExample.sh,v 1.1 2018-11-07 22:22:43 lsipusr Exp $"
# *CopyLeft*
# Copyright (c) 2011 Neda Communications, Inc. -- http://www.neda.com
# See PLPC-120001 for restrictions.
# This is a Halaal Poly-Existential intended to remain perpetually Halaal.
####+END:

__author__="
* Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
"


####+BEGIN: bx:dblock:lsip:bash:seed-spec :types "seedActions.bash"
SEED="
*  /[dblock]/ /Seed/ :: [[file:/opt/public/osmt/bin/seedActions.bash]] | 
"
FILE="
*  /This File/ :: /de/bx/nne/dev-py/pypi/pkgs/roPerf/bearerTokenExample/dev/bin/roPerf-bearerTokenExample.sh 
"
if [ "${loadFiles}" == "" ] ; then
    /opt/public/osmt/bin/seedActions.bash -l $0 "$@" 
    exit $?
fi
####+END:


_CommentBegin_
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/topControls.org"
*      ================
*  /Controls/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]] 
####+END:
_CommentEnd_

_CommentBegin_
*      ================
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]] CONTENTS-LIST ################
*  [[elisp:(org-cycle)][| ]]  Notes         :: *[Current-Info:]*  Status, Notes (Tasks/Todo Lists, etc.) [[elisp:(org-cycle)][| ]]
_CommentEnd_

function vis_moduleDescription {  cat  << _EOF_
*  [[elisp:(org-cycle)][| ]]  Xrefs         :: *[Related/Xrefs:]*  <<Xref-Here->>  -- External Documents  [[elisp:(org-cycle)][| ]]
**  [[elisp:(org-cycle)][| ]]  Panel        :: [[file:/libre/ByStar/InitialTemplates/activeDocs/bxServices/versionControl/fullUsagePanel-en.org::Xref-VersionControl][Panel Roadmap Documentation]] [[elisp:(org-cycle)][| ]]
*  [[elisp:(org-cycle)][| ]]  Info          :: *[Module Description:]* [[elisp:(org-cycle)][| ]]

_EOF_
}

_CommentBegin_
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]  *Seed Extensions*
_CommentEnd_

_CommentBegin_
*  [[elisp:(org-cycle)][| ]]  Imports       :: Prefaces (Imports/Libraries) [[elisp:(org-cycle)][| ]]
_CommentEnd_

. ${opBinBase}/lpInBaseDirDo.libSh

# PRE parameters

svcBaseName="bearerTokenExample"

#svcSpecPortNu=$( cat ./SvcSpec/defaultPortNu )
svcSpecPortNu="8080"

# /de/bx/nne/dev-py/pypi/pkgs/roPerf/bearerTokenExample/dev/roPerf/bearerTokenExample-base/svcSpec
workaroundBaseDir="/de/bx/nne/dev-py/pypi/pkgs/roPerf/bearerTokenExample"

svcSpecYaml="/de/bx/nne/dev-py/pypi/pkgs/roPerf/bearerTokenExample/dev/roPerf/bearerTokenExample-base/svcSpec/${svcBaseName}.yaml"
svcSpecJson="/de/bx/nne/dev-py/pypi/pkgs/roPerf/bearerTokenExample/dev/roPerf/bearerTokenExample-base/svcSpec/${svcBaseName}.json"
svcSpecJsonDeref="/de/bx/nne/dev-py/pypi/pkgs/roPerf/bearerTokenExample/dev/roPerf/bearerTokenExample-base/svcSpec/${svcBaseName}Deref.json"


function G_postParamHook {
     return 0
}


_CommentBegin_
*  [[elisp:(org-cycle)][| ]]  Examples      :: Examples [[elisp:(org-cycle)][| ]]
_CommentEnd_


function vis_examples {
    typeset extraInfo="-h -v -n showRun"
    #typeset extraInfo=""
    typeset runInfo="-p ri=lsipusr:passive"

    typeset examplesInfo="${extraInfo} ${runInfo}"


    visLibExamplesOutput ${G_myName}
  cat  << _EOF_
$( examplesSeperatorTopLabel "${G_myName}" )
$( examplesSeperatorChapter "Web Services Manager" )
$( examplesSeperatorSection "Api CodeGen Performer Python Flask -- ${svcBaseName}" )
${G_myName} ${extraInfo} -i apiCodeGenPyFlask ${svcSpecYaml} /tmp/${svcBaseName}PerfGen
$( examplesSeperatorSection "Update All Generated Code -- ${svcBaseName}" )
${G_myName} ${extraInfo} -i updateAll ${svcSpecYaml} ${svcBaseName}
$( examplesSeperatorSection "Start PyFLask Server -- ${svcBaseName}" )
${G_myName} ${extraInfo} -i serverStart /de/bx/nne/dev-py/pypi/pkgs/roPerf/bearerTokenExample/dev/roPerf/bearerTokenExample-base /tmp/${svcBaseName}PerfGen 
$( examplesSeperatorSection "Clean Generated Code -- ${svcBaseName}" )
${G_myName} ${extraInfo} -i codeGenClean ${svcBaseName}PerfGen
_EOF_
}

noArgsHook() {
  vis_examples
}

function vis_codeGenCliJar {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0  ]]

 
    cat  << _EOF_
/usr/local/bin/swagger-codegen-cli-2.2.2.jar
_EOF_

    lpReturn
}

function vis_updateAll {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 2  ]]

    local svcSpecInput="$1"
    local svcRootName="$2"

    opDo vis_apiCodeGenPyFlask "${svcSpecInput}" "${svcRootName}PerfGen"

    lpReturn
}



function vis_apiCodeGenPyFlask {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 2  ]]

    local svcSpecInput="$1"
    local generatedOutput="$2"

    local codegenCli=$( vis_codeGenCliJar )

    #
    # NOTYET, if generated output exists keep it in a safe place
    #

    echo "Generating Python code ..."
    opDo java -jar ${codegenCli} generate \
      -i "${svcSpecInput}" \
      -l python-flask \
      -o "${generatedOutput}"

    lpReturn
}


function vis_serverStart {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 2  ]]

    local controllerBaseDir="$1"
    local serverBaseDir="$2"

    # ./bearerTokenIssuerPerfGen/swagger_server/controllers
    opDo cp ${controllerBaseDir}/controllers/*.py ${serverBaseDir}/swagger_server/controllers

    inBaseDirDo ${serverBaseDir} grep http README.md

    source /bisos/venv/py3-bisos-3/bin/activate

    inBaseDirDo ${serverBaseDir} python3 -m swagger_server

    deactivate
    
    lpReturn
}


function vis_codeGenClean {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -gt 0  ]]

    local serverBaseDir=""    
    
    for serverBaseDir in $@ ;  do
	if [ -d "${serverBaseDir}" ] ; then
	    opDo rm -r "${serverBaseDir}"
	else
	    ANT_raw "Skipping Cleaning Of ${serverBaseDir}"
	fi
    done

    lpReturn
}




_CommentBegin_
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]  *End Of Editable Text*
_CommentEnd_

####+BEGIN: bx:dblock:bash:end-of-file :type "basic"
_CommentBegin_
*  [[elisp:(org-cycle)][| ]]  Common        ::  /[dblock] -- End-Of-File Controls/ [[elisp:(org-cycle)][| ]]
_CommentEnd_
#+STARTUP: showall
#local variables:
#major-mode: sh-mode
#fill-column: 90
# end:
####+END:
