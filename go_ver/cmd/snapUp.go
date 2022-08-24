/*
Copyright © 2022 Dean Hsu dean.xu.2357@gmail.com
*/
package cmd

import (
	"bytes"
	"errors"
	"fmt"
	"image"
	"image/png"
	"os"
	"time"

	"github.com/spf13/cobra"
	"github.com/tebeka/selenium"
	"github.com/tebeka/selenium/chrome"
	"pb_crawler/config"
)

// snapUpCmd represents the snapUp command.
var snapUpCmd = &cobra.Command{
	Use:   "snapUp [time string]",
	Short: "於指定時間搶購商品",
	Long:  `於指定時間搶購商品。時間格式為 "YYYY-MM-DD hh:mm:ss 時區(+8)"`,
	RunE:  snapUpRun,
}

func init() {
	rootCmd.AddCommand(snapUpCmd)

	snapUpCmd.Flags().BoolP("checkout", "c", false, "是否印出超商付款")
}

func snapUpRun(cmd *cobra.Command, args []string) error {
	fmt.Println("snapUp called")

	cfg := config.New()

	executeTime, err := time.Parse("2006-01-02 15:04:05 -07", args[0])
	if err != nil {
		return err
	}

	if time.Now().Local().After(executeTime) {
		return errors.New("time string expired")
	}

	service, err := selenium.NewChromeDriverService(
		cfg.Chromedriver,
		cfg.Port,
	)
	if err != nil {
		return err
	}
	defer service.Stop()

	caps := selenium.Capabilities{"browserName": "chrome"}
	caps.AddChrome(chrome.Capabilities{Args: []string{
		"--window-size=1920,1080",
		"--start-maximized",
		"--headless",
		"--no-sandbox",
		"--incognito",
		"--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7",
	}})
	wd, err := selenium.NewRemote(caps, fmt.Sprintf("http://127.0.0.1:%d/wd/hub", cfg.Port))
	if err != nil {
		return err
	}
	defer wd.Quit()

	if err := wd.Get(cfg.ProductUrl); err != nil {
		return fmt.Errorf("to page (%s) error: %w", cfg.ProductUrl, err)
	}

	loginBtn, err := wd.FindElement(selenium.ByXPATH, "/html/body/header/div[1]/div[4]/a/i")
	if err != nil {
		return fmt.Errorf("find login btn err: %w", err)
	}
	if err := loginBtn.Click(); err != nil {
		return fmt.Errorf("click login btn error: %w", err)
	}

	if err2 := loginFlow(wd, cfg); err2 != nil {
		return err2
	}

	fmt.Println("blocking")
	timer := time.NewTimer(time.Until(executeTime))
	defer timer.Stop()
	<-timer.C

	fmt.Printf("execute... %s\n", time.Now().String())

	if err2 := wd.Get(cfg.ProductUrl); err2 != nil {
		return fmt.Errorf("to page (%s), error: %w", cfg.ProductUrl, err2)
	}

	quantitySelect, err3 := wd.FindElement(selenium.ByXPATH, "/html/body/div[1]/div/main/section/section[1]/div[1]/div[2]/form/ul/li/div/select")
	if err3 != nil {
		return fmt.Errorf("find quantity select error: %w", err3)
	}
	if err3 := quantitySelect.Click(); err3 != nil {
		return fmt.Errorf("click quantity select error: %w", err3)
	}
	qSelect, err4 := wd.FindElement(selenium.ByXPATH, fmt.Sprintf("/html/body/div[1]/div/main/section/section[1]/div[1]/div[2]/form/ul/li/div/select/option[%d]", cfg.Quantity))
	if err4 != nil {
		return fmt.Errorf("find select option error: %w", err4)
	}
	if err4 := qSelect.Click(); err4 != nil {
		return fmt.Errorf("click select option error: %w", err4)
	}

	addToCartBtn, err := wd.FindElement(selenium.ByXPATH, "/html/body/div[1]/div/main/section/section[1]/div[1]/div[2]/form/div/button")
	if err != nil {
		return fmt.Errorf("find cart btn error: %w", err)
	}
	if err := addToCartBtn.Click(); err != nil {
		return fmt.Errorf("click cart btn error: %w", err)
	}

	if err := wd.WaitWithTimeoutAndInterval(func(wd selenium.WebDriver) (bool, error) {
		toCart, err := wd.FindElement(selenium.ByXPATH, "/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[3]/a")
		if err != nil {
			return false, nil
		}

		return toCart.IsDisplayed()
	}, 5*time.Second, 500*time.Millisecond); err != nil {
		return fmt.Errorf("waitWithTimeoutAndInterval error: %w", err)
	}

	checkout, err2 := cmd.Flags().GetBool("checkout")
	if err2 != nil {
		return fmt.Errorf("get flag error : %w", err2)
	}
	if checkout {
		toCart, err := wd.FindElement(selenium.ByXPATH, "/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[3]/a")
		if err != nil {
			return fmt.Errorf("find to cart error: %w", err)
		}
		if err := toCart.Click(); err != nil {
			return fmt.Errorf("client to cart error: %w", err)
		}
	}

	pic, err := wd.Screenshot()
	if err != nil {
		return fmt.Errorf("screen shot error : %w", err)
	}

	if err2 := picToFile(pic); err2 != nil {
		return err2
	}

	return nil
}

func picToFile(pic []byte) error {
	img, _, err := image.Decode(bytes.NewReader(pic))
	if err != nil {
		return fmt.Errorf("image decode error: %w", err)
	}

	file, err := os.Create("screen_shot.png")
	if err != nil {
		return fmt.Errorf("f create : %w", err)
	}
	defer file.Close()

	if err := png.Encode(file, img); err != nil {
		return err
	}
	return nil
}

func loginFlow(wd selenium.WebDriver, c *config.Config) error {
	if err := wd.WaitWithTimeoutAndInterval(
		func(wd selenium.WebDriver) (bool, error) {
			accountInput, err := wd.FindElement(selenium.ByXPATH, "/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[1]/div[1]/div[2]/label/input")
			if err != nil {
				return false, nil
			}
			return accountInput.IsDisplayed()
		},
		5*time.Second,
		300*time.Millisecond,
	); err != nil {
		return err
	}

	accountInput, err := wd.FindElement(selenium.ByXPATH, "/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[1]/div[1]/div[2]/label/input")
	if err != nil {
		return fmt.Errorf("find accountInput input error: %w", err)
	}
	if err := accountInput.SendKeys(c.Account); err != nil {
		return fmt.Errorf("accountInput send key error : %w", err)
	}

	pwdInput, err := wd.FindElement(selenium.ByXPATH, "/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[1]/div[2]/div[2]/label/input")
	if err != nil {
		return fmt.Errorf("find pwd input error : %w", err)
	}
	if err := pwdInput.SendKeys(c.Password); err != nil {
		return fmt.Errorf("pwd input send key failed: %w", err)
	}

	submitBtn, err := wd.FindElement(selenium.ByXPATH, "/html/body/div[1]/div/main/section/form/div[2]/div[1]/section/div[2]/div[2]/button/a")
	if err != nil {
		return fmt.Errorf("find submit btn error: %w", err)
	}
	if err := submitBtn.Click(); err != nil {
		return fmt.Errorf("click submit btn error: %w", err)
	}
	return nil
}
