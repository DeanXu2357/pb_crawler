/*
Copyright © 2022 Dean Hsu dean.xu.2357@gmail.com

*/
package cmd

import (
	"bytes"
	"fmt"
	"github.com/spf13/cobra"
	"github.com/tebeka/selenium"
	"github.com/tebeka/selenium/chrome"
	"image"
	"image/png"
	"os"
	"pb_crawler/config"
)

// snapUpCmd represents the snapUp command
var snapUpCmd = &cobra.Command{
	Use:   "snapUp [time string]",
	Short: "",
	Long:  ``,
	RunE:  snapUpRun,
}

func init() {
	rootCmd.AddCommand(snapUpCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// snapUpCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// snapUpCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}

func snapUpRun(cmd *cobra.Command, args []string) error {
	fmt.Println("snapUp called")

	c := config.New()

	//t, err := time.Parse("2006-01-02 15:04:05", args[0])
	//if err != nil {
	//	return err
	//}
	//
	//if t.After(time.Now()) {
	//	return errors.New("time string expired")
	//}

	//selenium.SetDebug(true)
	service, err := selenium.NewChromeDriverService(
		c.Chromedriver,
		c.Port,
		//selenium.StartFrameBuffer(), // Start an X frame buffer for the browser to run in.
		//selenium.Output(os.Stderr), // Output debug information to STDERR.
	)
	if err != nil {
		return err
	}
	defer service.Stop()

	caps := selenium.Capabilities{"browserName": "chrome"}
	caps.AddChrome(chrome.Capabilities{Args: []string{"--window-size=1920,1080", "--start-maximized", "--headless", "--no-sandbox", "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7"}})
	wd, err := selenium.NewRemote(caps, fmt.Sprintf("http://127.0.0.1:%d/wd/hub", c.Port))
	if err != nil {
		return err
	}
	defer wd.Quit()

	if err := wd.Get(c.ProductUrl); err != nil {
		return fmt.Errorf("to page (%s) error: %w", c.ProductUrl, err)
	}

	loginBtn, err := wd.FindElement(selenium.ByXPATH, "/html/body/header/div[1]/div[4]/a/i")
	if err != nil {
		return fmt.Errorf("find login btn err: %w", err)
	}
	if err := loginBtn.Click(); err != nil {
		return fmt.Errorf("click login btn error: %w", err)
	}

	pic, err := wd.Screenshot()
	if err != nil {
		return fmt.Errorf("screen shot error : %w", err)
	}

	img, _, err := image.Decode(bytes.NewReader(pic))
	if err != nil {
		return fmt.Errorf("image decode error: %w", err)
	}

	f, err := os.Create("screen_shot.png")
	if err != nil {
		return fmt.Errorf("f create : %w", err)
	}
	defer f.Close()

	if err := png.Encode(f, img); err != nil {
		return err
	}

	return nil
}
