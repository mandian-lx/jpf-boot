%{?_javapackages_macros:%_javapackages_macros}

%define bname jpf

Summary:	Boot plug-in for the Java Plug-in FrameworkPlugin
Name:		%{bname}-boot
Version:	1.5.1
Release:	1
License:	LGPLv2.1
Group:		Development/Java
URL:		http://jpf.sourceforge.net/
Source0:	http://sourceforge.net/projects/%{bname}/files/%{bname}-%(cut -d\. -f-2 <<<%{version})/%{bname}-%{version}/%{bname}-src-%{version}.zip
BuildArch:	noarch

BuildRequires:  maven-local
BuildRequires:  mvn(log4j:log4j)
BuildRequires:  mvn(net.sf.jpf:jpf)

%description
This package contains helper classes to start/stop JPF based applications.

%files -f .mfiles
%doc README.txt
%doc BUILD.txt
%doc MAVEN.txt
%doc changelog.txt
%doc license.txt

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation
Requires:	jpf-javadoc

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc license.txt

#----------------------------------------------------------------------------

%prep
%setup -q -c %{bname}-src-%{version}

# Delete all pre-built binaries
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Fix missing version
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-compiler-plugin']]" "
	<version>any</version>" %{name}-pom.xml
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]" "
	<version>any</version>" %{name}-pom.xml

# Remove the classpath from the manifest file
%pom_xpath_remove "pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]/pom:configuration/pom:archive/pom:manifest" %{name}-pom.xml

# Fix jar-not-indexed warning
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]/pom:configuration/pom:archive" "
	<index>true</index>" %{name}-pom.xml

# Fix Jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build -- -f %{name}-pom.xml -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

