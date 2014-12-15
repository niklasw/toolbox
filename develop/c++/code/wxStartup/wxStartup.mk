##
## Auto Generated makefile by CodeLite IDE
## any manual changes will be erased      
##
## Debug
ProjectName            :=wxStartup
ConfigurationName      :=Debug
WorkspacePath          := "/home/niklas/toolbox/develop/c++/code/wxStartup"
ProjectPath            := "/home/niklas/toolbox/develop/c++/code/wxStartup"
IntermediateDirectory  :=./Debug
OutDir                 := $(IntermediateDirectory)
CurrentFileName        :=
CurrentFilePath        :=
CurrentFileFullPath    :=
User                   :=niklas
Date                   :=05/21/14
CodeLitePath           :="/home/niklas/.codelite"
LinkerName             :=g++
SharedObjectLinkerName :=g++ -shared -fPIC
ObjectSuffix           :=.o
DependSuffix           :=.o.d
PreprocessSuffix       :=.o.i
DebugSwitch            :=-gstab
IncludeSwitch          :=-I
LibrarySwitch          :=-l
OutputSwitch           :=-o 
LibraryPathSwitch      :=-L
PreprocessorSwitch     :=-D
SourceSwitch           :=-c 
OutputFile             :=$(IntermediateDirectory)/$(ProjectName)
Preprocessors          :=
ObjectSwitch           :=-o 
ArchiveOutputSwitch    := 
PreprocessOnlySwitch   :=-E 
ObjectsFileList        :="wxStartup.txt"
PCHCompileFlags        :=
MakeDirCommand         :=mkdir -p
LinkOptions            :=  $(shell wx-config --libs --debug)
IncludePath            :=  $(IncludeSwitch). $(IncludeSwitch). 
IncludePCH             := 
RcIncludePath          := 
Libs                   := 
ArLibs                 :=  
LibPath                := $(LibraryPathSwitch). 

##
## Common variables
## AR, CXX, CC, AS, CXXFLAGS and CFLAGS can be overriden using an environment variables
##
AR       := ar rcus
CXX      := g++
CC       := gcc
CXXFLAGS :=  -g -O0 -Wall $(shell wx-config --cflags --debug) $(Preprocessors)
CFLAGS   :=  -g -O0 -Wall $(Preprocessors)
ASFLAGS  := 
AS       := as


##
## User defined environment variables
##
CodeLiteDir:=/usr/share/codelite
Objects0=$(IntermediateDirectory)/main$(ObjectSuffix) $(IntermediateDirectory)/MainFrame$(ObjectSuffix) $(IntermediateDirectory)/wxcrafter$(ObjectSuffix) $(IntermediateDirectory)/wxcrafter_bitmaps$(ObjectSuffix) 



Objects=$(Objects0) 

##
## Main Build Targets 
##
.PHONY: all clean PreBuild PrePreBuild PostBuild
all: $(OutputFile)

$(OutputFile): $(IntermediateDirectory)/.d $(Objects) 
	@$(MakeDirCommand) $(@D)
	@echo "" > $(IntermediateDirectory)/.d
	@echo $(Objects0)  > $(ObjectsFileList)
	$(LinkerName) $(OutputSwitch)$(OutputFile) @$(ObjectsFileList) $(LibPath) $(Libs) $(LinkOptions)

$(IntermediateDirectory)/.d:
	@test -d ./Debug || $(MakeDirCommand) ./Debug

PreBuild:


##
## Objects
##
$(IntermediateDirectory)/main$(ObjectSuffix): main.cpp $(IntermediateDirectory)/main$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/niklas/toolbox/develop/c++/code/wxStartup/main.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/main$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/main$(DependSuffix): main.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/main$(ObjectSuffix) -MF$(IntermediateDirectory)/main$(DependSuffix) -MM "main.cpp"

$(IntermediateDirectory)/main$(PreprocessSuffix): main.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/main$(PreprocessSuffix) "main.cpp"

$(IntermediateDirectory)/MainFrame$(ObjectSuffix): MainFrame.cpp $(IntermediateDirectory)/MainFrame$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/niklas/toolbox/develop/c++/code/wxStartup/MainFrame.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/MainFrame$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/MainFrame$(DependSuffix): MainFrame.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/MainFrame$(ObjectSuffix) -MF$(IntermediateDirectory)/MainFrame$(DependSuffix) -MM "MainFrame.cpp"

$(IntermediateDirectory)/MainFrame$(PreprocessSuffix): MainFrame.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/MainFrame$(PreprocessSuffix) "MainFrame.cpp"

$(IntermediateDirectory)/wxcrafter$(ObjectSuffix): wxcrafter.cpp $(IntermediateDirectory)/wxcrafter$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/niklas/toolbox/develop/c++/code/wxStartup/wxcrafter.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/wxcrafter$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/wxcrafter$(DependSuffix): wxcrafter.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/wxcrafter$(ObjectSuffix) -MF$(IntermediateDirectory)/wxcrafter$(DependSuffix) -MM "wxcrafter.cpp"

$(IntermediateDirectory)/wxcrafter$(PreprocessSuffix): wxcrafter.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/wxcrafter$(PreprocessSuffix) "wxcrafter.cpp"

$(IntermediateDirectory)/wxcrafter_bitmaps$(ObjectSuffix): wxcrafter_bitmaps.cpp $(IntermediateDirectory)/wxcrafter_bitmaps$(DependSuffix)
	$(CXX) $(IncludePCH) $(SourceSwitch) "/home/niklas/toolbox/develop/c++/code/wxStartup/wxcrafter_bitmaps.cpp" $(CXXFLAGS) $(ObjectSwitch)$(IntermediateDirectory)/wxcrafter_bitmaps$(ObjectSuffix) $(IncludePath)
$(IntermediateDirectory)/wxcrafter_bitmaps$(DependSuffix): wxcrafter_bitmaps.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) -MG -MP -MT$(IntermediateDirectory)/wxcrafter_bitmaps$(ObjectSuffix) -MF$(IntermediateDirectory)/wxcrafter_bitmaps$(DependSuffix) -MM "wxcrafter_bitmaps.cpp"

$(IntermediateDirectory)/wxcrafter_bitmaps$(PreprocessSuffix): wxcrafter_bitmaps.cpp
	@$(CXX) $(CXXFLAGS) $(IncludePCH) $(IncludePath) $(PreprocessOnlySwitch) $(OutputSwitch) $(IntermediateDirectory)/wxcrafter_bitmaps$(PreprocessSuffix) "wxcrafter_bitmaps.cpp"


-include $(IntermediateDirectory)/*$(DependSuffix)
##
## Clean
##
clean:
	$(RM) $(IntermediateDirectory)/main$(ObjectSuffix)
	$(RM) $(IntermediateDirectory)/main$(DependSuffix)
	$(RM) $(IntermediateDirectory)/main$(PreprocessSuffix)
	$(RM) $(IntermediateDirectory)/MainFrame$(ObjectSuffix)
	$(RM) $(IntermediateDirectory)/MainFrame$(DependSuffix)
	$(RM) $(IntermediateDirectory)/MainFrame$(PreprocessSuffix)
	$(RM) $(IntermediateDirectory)/wxcrafter$(ObjectSuffix)
	$(RM) $(IntermediateDirectory)/wxcrafter$(DependSuffix)
	$(RM) $(IntermediateDirectory)/wxcrafter$(PreprocessSuffix)
	$(RM) $(IntermediateDirectory)/wxcrafter_bitmaps$(ObjectSuffix)
	$(RM) $(IntermediateDirectory)/wxcrafter_bitmaps$(DependSuffix)
	$(RM) $(IntermediateDirectory)/wxcrafter_bitmaps$(PreprocessSuffix)
	$(RM) $(OutputFile)
	$(RM) ".build-debug/wxStartup"


