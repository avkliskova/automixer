let pkgs = import <nixpkgs> {};
in pkgs.mkShell {
        buildInputs = with pkgs; [
          bpm-tools
          ffmpeg
          keyfinder-cli
          sox
          python3Packages.youtube-dl
        ];
}
