{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.chromium
    pkgs.chromedriver
    pkgs.undetected-chromedriver
    pkgs.python3
    pkgs.python3.pkgs.selenium
    pkgs.python3.pkgs.undetected-chromedriver
  ];

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.glibc}/lib:${pkgs.glib}/lib";

  shellHook = ''
    export CHROME_PATH="${pkgs.chromium}/bin/chromium"
    export CHROMEDRIVER_PATH="${pkgs.chromedriver}/bin/chromedriver"
    echo "Chrome version: $(chromium --version)"
    echo "ChromeDriver version: $(chromedriver --version)"
    echo "Python version: $(python3 --version)"
    echo "Undetected-chromedriver path: $(which undetected-chromedriver)"
  '';
}
