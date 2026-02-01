package cmd

import (
	"fmt"
	"os"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
  Use:   "zxdf",
  Short: "package manager for prompts",
  Long: "package manager for prompts",
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Print("Hello world\n")
  },
}

func Execute() {
  if err := rootCmd.Execute(); err != nil {
    fmt.Fprintln(os.Stderr, err)
    os.Exit(1)
  }
}

