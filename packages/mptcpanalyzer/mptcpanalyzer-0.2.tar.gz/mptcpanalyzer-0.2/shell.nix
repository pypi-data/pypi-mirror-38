{ pkgs ? import <nixpkgs> {} }:
let
  m = pkgs.mptcpanalyzer.overrideAttrs (oa: {

    propagatedBuildInputs = oa.propagatedBuildInputs ++ [
      # to publish on pypi
      pkgs.python3Packages.twine
    ];

    src = ./.;
  });
in
    m
