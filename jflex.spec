%bcond_without bootstrap

Summary:	A Lexical Analyzer Generator for Java
Name:		jflex
Version:	1.4.3
Release:	1
License:	GPLv2
Group:		Development/Java
Url:		http://www.jflex.de/
Source0:	http://www.jflex.de/jflex-%version.tar.gz
Source1:	jflex.script
Source2:	jflex-1.4.3-generated-files.tar.bz2
Patch0:		jflex-javac-no-target.patch
Patch1:		jflex-no-cup-no-jflex.patch
Patch2:		jflex-classpath.patch
Patch4:		jflex-byaccj-utl.patch
BuildArch:	noarch

BuildRequires:	ant
BuildRequires:	java_cup
BuildRequires:	java-1.6.0-openjdk-devel
%if %without bootstrap
BuildRequires:	jflex >= 0:1.4.3-1
%endif
BuildRequires:	java-rpmbuild
BuildRequires:	junit
BuildRequires:	locales-en
Requires:	java_cup
Requires:	jpackage-utils

%track
prog %name = {
	url = http://www.jflex.de/download.html
	regex = %name-(__VER__)\.tar\.gz
	version = %version
}

%description
JFlex is a lexical analyzer generator for Java written in Java. It is 
also a rewrite of the very useful tool JLex which was developed by 
Elliot Berk at Princeton University. As Vern Paxson states for his C/C++ 
tool flex:	they do not share any code though.

Design goals The main design goals of JFlex are:

    * Full unicode support
    * Fast generated scanners
    * Fast scanner generation
    * Convenient specification syntax
    * Platform independence
    * JLex compatibility

%package javadoc
Group:		Development/Java
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
rm -rf src/java_cup
find . -name '*.jar' | xargs -t rm
%patch0 -p1
%if %with bootstrap
%setup -q -T -D -a 2
%patch1 -p1
%else
%patch2 -p1
%patch4 -p1
%endif

%build
export LC_ALL=ISO-8859-1
pushd src
%if %without bootstrap
export CLASSPATH=$(build-classpath java-cup junit jflex)
%else
export CLASSPATH=$(build-classpath java-cup junit)
%endif
export JAVA_HOME=%{_prefix}/lib/jvm/java-1.6.0
export OPT_JAR_LIST=
%if %without bootstrap
ant realclean
%endif
ant jar
mkdir -p ../dist/docs/api
javadoc -d ../dist/docs/api `find . -type f -name "*.java"`
popd

%install
# jar
mkdir -p %{buildroot}%{_javadir}
install -m 644 lib/JFlex.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -s ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# compatibility symlink
(cd %{buildroot}%{_javadir} && ln -s jflex.jar JFlex.jar)
# javadoc
mkdir -p 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -s %{name}-%{version} %{name})

mkdir -p %{buildroot}%{_bindir}
install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/jflex

sed -i -e 's/\r$//g' examples/standalone/sample.inp

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%doc COPYRIGHT doc examples src/README src/changelog
%attr(0755,root,root) %{_bindir}/jflex
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/JFlex.jar

%files javadoc
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

