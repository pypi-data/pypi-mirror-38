        # remove from the matrix poor or duplicated bins
        #self.remove_unreliable_rows()
        #log.debug("Size of matrix is {}".format(self.hic.matrix.shape[0]))


@ this line was found after reducing the matrix
# put a high value to all edges belonging to an original path
max_int = self.cmatrix.data.max()+1


    def remove_unreliable_rows(self, min_coverage=MIN_COVERAGE):
        """
        identifies rows that are too small.  Those rows will be
        excluded from any computation.

        Parameters
        ----------
        min_coverage

        Returns
        -------
        None: The matrix object is edited in place

        """
        log.debug("filtering unreliable contigs")
        contig_id, c_start, c_end, coverage = zip(*self.hic.cut_intervals)

        # get length of each contig
        length = np.array(c_end) - np.array(c_start)

        # get the list of bins that have too few interactions to other
        from hicexplorer.hicCorrectMatrix import MAD
        self.hic.matrix.data[np.isnan(self.hic.matrix.data)] = 0
        row_sum = np.asarray(self.hic.matrix.sum(axis=1)).flatten()
        row_sum = row_sum - self.hic.matrix.diagonal()
        mad = MAD(row_sum)
        modified_z_score = mad.get_motified_zscores()
        log.debug("self.min_mad = {} counts".format(mad.mad_to_value(self.min_mad)))
        few_inter = np.flatnonzero(modified_z_score < self.min_mad)
        log.debug("self.max_mad = {} counts".format(mad.mad_to_value(self.max_mad)))
        repetitive = np.flatnonzero(modified_z_score > self.max_mad)

        # get list of bins that have reduced coverage:
        low_cov_list = np.flatnonzero(np.array(coverage) < min_coverage)

        to_remove = np.unique(np.hstack([few_inter, low_cov_list, repetitive]))

        rows_to_keep = cols_to_keep = np.delete(range(self.hic.matrix.shape[1]), to_remove)
        log.info("Total bins: {}, few inter: {}, low cover: {}, "
                 "repetitive: {}".format(len(contig_id),
                                         len(few_inter),
                                         len(low_cov_list),
                                         len(repetitive)))
        if len(to_remove) >= self.hic.matrix.shape[0] * 0.7:
            log.error("Filtering to strong. 70% of all regions would be removed.")
            exit(0)

        log.info("{}: removing {} ({:.2f}%) low quality regions from hic matrix\n"
                 "having less than {} interactions to other contigs.\n\n"
                 "Keeping {} bins.\n ".format(inspect.stack()[0][3], len(to_remove),
                                              100 * float(len(to_remove))/self.hic.matrix.shape[0],
                                              mad.mad_to_value(self.min_mad), len(rows_to_keep)))
        total_length = sum(length)
        removed_length = sum(length[to_remove])
        kept_length = sum(length[rows_to_keep])

        log.info("Total removed length:{:,} ({:.2f}%)\nTotal "
                 "kept length: {:,}({:.2f}%)".format(removed_length,
                                                     float(removed_length) / total_length,
                                                     kept_length,
                                                     float(kept_length) / total_length))
        # remove rows and cols from matrix
        new_matrix = self.hic.matrix[rows_to_keep, :][:, cols_to_keep]
        new_cut_intervals = [self.hic.cut_intervals[x] for x in rows_to_keep]

        # some rows may have now 0 read counts, remove them as well
        to_keep = np.flatnonzero(np.asarray(new_matrix.sum(1)).flatten() > 0)
        if len(to_keep) != new_matrix.shape[0]:
            print "removing {} extra rows that after filtering ended up "\
                "with no interactions".format(new_matrix.shape[0] - len(to_keep))
            new_matrix = new_matrix[to_keep, :][:, to_keep]
            new_cut_intervals = [new_cut_intervals[x] for x in to_keep]
        self.hic.update_matrix(new_matrix, new_cut_intervals)
        return self.hic


    @staticmethod
    def expand_old(alist):
        """
        To reduce the number of permutations tested
        some pairs are fixed, meaning that they
        should always be together. Thus, the pair
        is treated like one item and the number of
        permutations is reduced. However, each pair
        can be as either (a,b) or (b,a).
        This code expands the original list
        adding pairs in both directions

        The fixed pairs are encoded as an string like ',1,2'

        Parameters
        ----------
        alist : list of integers and str where the str indicate fixed paths

        >>> Scaffolds.permute_paths([',1,2'])
        [[1, 2], [2, 1]]
        >>> Scaffolds.permute_paths([',1,2', 3])
        [[1, 2, 3], [2, 1, 3]]
        >>> Scaffolds.permute_paths([1,2, ',3,4',5])
        [[1, 2, 3, 4, 5], [1, 2, 4, 3, 5]]
        >>> Scaffolds.permute_paths([1,',2,3', 4, ',5,6'])
        [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 6, 5], [1, 3, 2, 4, 5, 6], [1, 3, 2, 4, 6, 5]]
        >>> Scaffolds.permute_paths([',1,2', ',3,4', ',5,6'])[0:3]
        [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 6, 5], [1, 2, 4, 3, 5, 6]]
        >>> Scaffolds.permute_paths([1,2,3])
        [[1, 2, 3]]
        """
        ret = []
        expand_vals = []
        positions = [-1]
        # identify positions to expand
        for idx, val in enumerate(alist):
            try:
                if val[0] == ",":
                    path = [int(x) for x in val.split(",")[1:]]
                    expand_vals.append(path)
                    positions.append(idx)
            except (IndexError, TypeError):
                # the exception happens when val is an int
                continue
        if not len(expand_vals):
            return [alist]
        # expand the list
        for prod in itertools.product(*[(0, 1)]*len(expand_vals)):
            new_list = []
            for idx, pair in enumerate(expand_vals):
                new_list += alist[positions[idx]+1:positions[idx+1]]
                # a bitwise operator is used to decide
                # if the pair should be flipped or not
                pair = pair if prod[idx] == 0 else pair[::-1]
                new_list += pair
            if len(alist) > idx+1:
                new_list += alist[positions[idx+1]+1:]
            ret.append(new_list)
        return ret
