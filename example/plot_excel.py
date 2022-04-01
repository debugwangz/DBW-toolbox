def plot_excel_measrues(excel_name, measures):
    fnames = []
    for sparse_num in sparse_nums:
        fname = 'measures_{}.xls'.format(sparse_num)
        fnames.append(fname)
    sorted(os.listdir(indicator_path))

    measures = {}


    for fname in fnames:
        df = pd.read_excel(ospj(indicator_path, fname))

        for i in range(len(mapping_names.keys())):
            if df.loc[i,'methods'] not in mapping_names.keys():
                print('{} not in keys'.format(df.loc[i,'methods']))
                continue
            method = mapping_names[df.loc[i,'methods']]
            ssim = df.loc[i,'ssim']
            mse = df.loc[i,'mse']
            if not method in measures:
                measures[method] = {}
            measure = measures[method]
            if not 'ssim' in measure:
                measure['ssim'] = []
                measure['mse'] = []
                measure['gradient'] = []

            ssim_list = measure['ssim']
            mse_list = measure['mse']
            ssim_list.append(ssim)
            mse_list.append(mse)
    for method_name, i in zip(measures.keys(), range(len(measures.keys()))):
        measure = measures[method_name]
        ssim = measure['ssim']
        # for j in range(3):
        #     gradient_list = measure['gradient']
            # gradient_list.append((ssim[j + 1] - ssim[j]) / (sparse_nums[j + 1] - sparse_nums[j]))
        plt.plot(range(len(ssim)),ssim, label=method_name, marker=markers[i],
                 color=color_mappings[method_name],linewidth=1.5 )
        plt.xticks(range(len(ssim)),sparse_nums)

    plt.ylabel("SSIM")
    plt.xlabel("Projection views")

    plt.legend()
    plt.savefig(ospj(plot_save_path, 'plot_ssim.png'))
    # plt.show()
    plt.close()

    # gradient_labels = ['57-39', '75-57', '100-75']
    # for method_name, i in zip(measures.keys(), range(len(measures.keys()))):
    #     measure = measures[method_name]
    #     gradient = measure['gradient']
    #     plt.plot(range(len(gradient)), gradient, label=method_name, marker=markers[i])
    # #     plt.xticks(range(len(gradient)),gradient_labels)
    # plt.xlabel("Projection views")
    # plt.ylabel("Change rate of SSIM")
    # plt.legend()
    # # plt.show()
    # plt.savefig(ospj(plot_save_path, 'plot_ssim_gradient.png'))
    # plt.close()

    for method_name, i in zip(measures.keys(), range(len(measures.keys()))):
        measure = measures[method_name]
        mse = measure['mse']
        plt.plot(range(len(mse)), mse, label=method_name, marker=markers[i])
        plt.xticks(range(len(mse)), sparse_nums)
    plt.ylabel("MSE")
    plt.xlabel("Projection views")

    plt.legend()
    plt.savefig(ospj(plot_save_path, 'plot_mse.png'))
    # plt.show()
    plt.close()